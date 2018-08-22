import json
import os.path

import google.oauth2.credentials
import google_auth_oauthlib.flow


def _fetch_new_creds(config):
  return google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
      config, scopes=[
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/spreadsheets.readonly',
      ]).run_console()


def _create_and_save_tokens(token_path, config_path):
  with open(config_path, 'r') as config_file:
    config = json.load(config_file)
  credentials = _fetch_new_creds(config)
  keys = ('token', 'refresh_token', 'token_uri', 'client_id', 'client_secret',
          'scopes')
  with open(token_path, 'w') as token_file:
    json.dump({k: getattr(credentials, k) for k in keys}, token_file)


def creds(config_dir=os.path.expanduser('~/.emailer')):
  token_path = os.path.join(config_dir, 'token.json')
  if not os.path.exists(token_path):
    config_path = os.path.join(config_dir, 'client_secret.json')
    _create_and_save_tokens(token_path, config_path)
  with open(token_path, 'r') as token_file:
    return google.oauth2.credentials.Credentials(**json.load(token_file))


if __name__ == '__main__':
  creds()
