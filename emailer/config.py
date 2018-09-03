import dataclasses  # pylint: disable=wrong-import-order
import json
import os.path


CONFIG_FILES = ['.emailer.json', 'emailer.json']


class InvalidFileError(Exception):
  pass


class InvalidFileContentError(Exception):
  pass


@dataclasses.dataclass(frozen=True)
class Config():
  client_secret: dict = None
  serialized_creds: dict = None
  keys: dict = None

  def validate(self):
    if self.client_secret is None:
      raise InvalidFileContentError(
          'Unable to locate client_secret data: '
          'https://developers.google.com/identity/protocols/OAuth2')

  def get_keys(self, names=None):
    if self.keys is None:
      raise InvalidFileContentError('No keys dict in config.')
    if names is None:
      return self.keys.values()
    return (self.keys[name] for name in names)

  def set_serialized_creds(self, serialized_creds):
    return dataclasses.replace(self, serialized_creds=serialized_creds)

  def save_to_file(self, config_path):
    with open(config_path, 'w') as config_file:
      json.dump(dataclasses.asdict(self), config_file, indent=2, sort_keys=True)


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


def load_from_file(config_path):
  if not config_path or not os.path.exists(config_path):
    raise InvalidFileError(config_path)
  with open(config_path, 'r') as config_file:
    try:
      return Config(**json.load(config_file))
    except json.JSONDecodeError:
      raise InvalidFileContentError(f'{config_path} must be a valid JSON file.')
