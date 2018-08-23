import json
import os.path


def load(config_path):
  try:
    with open(config_path, 'r') as config_file:
      return json.load(config_file)
  except (ValueError, TypeError):
    return {}


def _create_and_save_tokens(token_path, config_path):
  with open(config_path, 'r') as config_file:
    config = json.load(config_file)
  credentials = _fetch_new_creds(config)
  with open(token_path, 'w') as token_file:
    json.dump({k: getattr(credentials, k) for k in keys}, token_file)


def old_creds(config_dir=os.path.expanduser('~/.emailer')):
  token_path = os.path.join(config_dir, 'token.json')
  if not os.path.exists(token_path):
    config_path = os.path.join(config_dir, 'client_secret.json')
    _create_and_save_tokens(token_path, config_path)
  with open(token_path, 'r') as token_file:
    return google.oauth2.credentials.Credentials(**json.load(token_file))
