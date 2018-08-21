import json
import os.path

import google.oauth2.credentials
import google_auth_oauthlib.flow


# https://developers.google.com/gmail/api/auth/scopes
# https://developers.google.com/sheets/api/guides/authorizing
_SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
]
_DEFAULT_CONFIG_DIR = os.path.expanduser('~/.emailer')
_CLIENT_SECRET_FILENAME = 'client_secret.json'
_TOKENS_FILENAME = 'token.json'
_CREDENTIAL_KEYS = ['token', 'refresh_token', 'token_uri', 'client_id',
                    'client_secret', 'scopes']


def _load_json_file(path):
  with open(path, 'r') as f:
    return json.load(f)


def _save_json_file(data, path):
  with open(path, 'w') as f:
    json.dump(data, path)


def _fetch_new_tokens(config):
  flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
      config, scopes=_SCOPES)
  creds = flow.run_console()
  return {k: getattr(creds, k) for k in _CREDENTIAL_KEYS}


def _create_tokens(token_path, config_path):
  config = _load_json_file(config_path)
  tokens = _fetch_new_tokens(config)
  _save_json_file(tokens, token_path)


def creds(config_dir=None):
  if config_dir is None:
    config_dir = _DEFAULT_CONFIG_DIR
  token_path = os.path.join(config_dir, _TOKENS_FILENAME)
  if not os.path.exists(token_path):
    config_path = os.path.join(config_dir, _CLIENT_SECRET_FILENAME)
    _create_tokens(token_path, config_path)
  return google.oauth2.credentials.Credentials(**_load_json_file(token_path))


if __name__ == '__main__':
  creds()
