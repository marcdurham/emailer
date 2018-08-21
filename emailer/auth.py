import json
import os.path

import google.oauth2.credentials
import google_auth_oauthlib.flow


def _load_json_file(path):
  with open(path, 'r') as f:
    return json.load(f)


def _save_json_file(data, path):
  with open(path, 'w') as f:
    json.dump(data, path)


def _fetch_new_creds(config):
  return google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
      config, scopes=[
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/spreadsheets.readonly',
      ]).run_console()


def _create_and_save_tokens(token_path, config_path):
  config = _load_json_file(config_path)
  creds = _fetch_new_creds(config)
  keys = ('token', 'refresh_token', 'token_uri', 'client_id', 'client_secret',
          'scopes')
  _save_json_file({k: getattr(creds, k) for k in keys}, token_path)


def creds(config_dir=os.path.expanduser('~/.emailer')):
  token_path = os.path.join(config_dir, 'token.json')
  if not os.path.exists(token_path):
    config_path = os.path.join(config_dir, 'client_secret.json')
    _create_and_save_tokens(token_path, config_path)
  return google.oauth2.credentials.Credentials(**_load_json_file(token_path))


if __name__ == '__main__':
  creds()
