import json
import os.path


CLIENT_SECRET_KEY = 'client_secret'
CONFIG_FILE = '.emailer/config.json'


class InvalidFileError(Exception):
  pass


class InvalidFileContentError(Exception):
  pass


def dirs(root):
  while True:
    dirname = os.path.dirname(root)
    yield os.path.join(root, CONFIG_FILE)
    if root == dirname:
      break
    root = dirname
  yield os.path.join(os.path.expanduser('~'), CONFIG_FILE)


def find(root):
  for path in dirs(root):
    if os.path.exists(path):
      return path
  return None


def load(config_path):
  if not config_path or not os.path.exists(config_path):
    raise InvalidFileError(config_path)
  with open(config_path, 'r') as config_file:
    try:
      return json.load(config_file)
    except json.JSONDecodeError:
      raise InvalidFileContentError(
          '{} must be a valid JSON file.'.format(config_path))


def validate(config):
  if CLIENT_SECRET_KEY not in config:
    raise InvalidFileContentError(
        'Unable to locate client_secret data, see {} to obtain one.'.format(
            'https://developers.google.com/identity/protocols/OAuth2'))


def save(config_path, config):
  with open(config_path, 'w') as config_file:
    json.dump(config, config_file)
