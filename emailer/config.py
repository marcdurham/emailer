import json
import os.path

import attr


CLIENT_SECRET_KEY = 'client_secret'
SERIALIZED_CREDS_KEY = 'serialized_creds'
CONFIG_FILES = ['.emailer.json', 'emailer.json']


@attr.s(frozen=True)
class Config():
  client_secret = attr.ib()
  serialized_creds = attr.ib()

  def set_serialized_creds(self, serialized_creds):
    new_attrs = attr.asdict(self, recurse=False)
    new_attrs[CLIENT_SECRET_KEY] = serialized_creds
    return Config(**new_attrs)

  def serialize(self):
    return attr.asdict(self)

  def save_to_file(self, config_path):
    with open(config_path, 'w') as config_file:
      json.dump(self.serialize(), config_file)


class InvalidFileError(Exception):
  pass


class InvalidFileContentError(Exception):
  pass


def files(root_path):
  for config_file in CONFIG_FILES:
    root = root_path
    while True:
      dirname = os.path.dirname(root)
      yield os.path.join(root, config_file)
      if root == dirname:
        break
      root = dirname
    yield os.path.join(os.path.expanduser('~'), config_file)


def find_config_file(root):
  for path in files(root):
    if os.path.exists(path):
      return path
  return None


def validate(config):
  if CLIENT_SECRET_KEY not in config:
    raise InvalidFileContentError(
        'Unable to locate client_secret data, see {} to obtain one.'.format(
            'https://developers.google.com/identity/protocols/OAuth2'))


def create_from_data(data):
  validate(data)
  return Config(
      client_secret=data[CLIENT_SECRET_KEY],
      serialized_creds=data.get(SERIALIZED_CREDS_KEY),
      )


def load_from_file(config_path):
  if not config_path or not os.path.exists(config_path):
    raise InvalidFileError(config_path)
  with open(config_path, 'r') as config_file:
    try:
      return create_from_data(json.load(config_file))
    except json.JSONDecodeError:
      raise InvalidFileContentError(
          '{} must be a valid JSON file.'.format(config_path))
