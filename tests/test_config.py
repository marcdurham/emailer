import json
import os.path

import pytest

from emailer import config


def test_load_none_file_raises_invalid_file_error():
  with pytest.raises(config.InvalidFileError, match='None'):
    config.load_from_file(None)


def test_load_nonexistent_file_raises_invalid_file_error(tmpdir):
  file_name = tmpdir.join('does_not_exist').strpath
  with pytest.raises(config.InvalidFileError, match=file_name):
    config.load_from_file(file_name)


def test_load_returns_filled_config_object(tmpdir):
  config_file = tmpdir.join('config.json')
  config_file.write(json.dumps(
    {'hi': 'bye', 'client_secret': 's', 'serialized_creds': 'world'}))
  config_data = config.load_from_file(config_file.strpath)
  assert config_data.serialized_creds == 'world'
  assert config_data.client_secret == 's'


def test_load_empty_file_raises_invalid_file_content_error(tmpdir):
  with pytest.raises(config.InvalidFileContentError, match='config.json'):
    config_file = tmpdir.join('config.json')
    config_file.write('')
    config.load_from_file(config_file.strpath)


def test_load_bad_json_file_raises_invalid_file_content_error(tmpdir):
  with pytest.raises(config.InvalidFileContentError, match='config.json'):
    config_file = tmpdir.join('config.json')
    config_file.write('badjson')
    config.load_from_file(config_file.strpath)


def test_create_from_empty_dict_fails_without_valid_client_secret_config():
  with pytest.raises(config.InvalidFileContentError, match='client_secret'):
    config.create_from_data({})


def test_save_updates_config_file_with_data(tmpdir):
  config_file = tmpdir.join('config.json')
  config_obj = config.create_from_data({config.CLIENT_SECRET_KEY: 'hi'})
  config_obj.save_to_file(config_file.strpath)
  assert json.loads(config_file.read())[config.CLIENT_SECRET_KEY] == 'hi'


def test_files_yields_all_possible_names():
  assert list(config.files('/test/one')) == [
      '/test/one/.emailer.json',
      '/test/.emailer.json',
      '/.emailer.json',
      os.path.expanduser('~/.emailer.json'),
      '/test/one/emailer.json',
      '/test/emailer.json',
      '/emailer.json',
      os.path.expanduser('~/emailer.json'),
      ]


def test_find_returns_first_existing_config_dot(tmpdir):
  config_file = tmpdir.join('emailer.json')
  config_file.write('')
  assert config.find_config_file(config_file.strpath) == config_file.strpath


def test_find_returns_none_if_no_existing_config(tmpdir, monkeypatch):
  monkeypatch.setattr(os.path, 'expanduser', lambda _: tmpdir.strpath)
  assert config.find_config_file(tmpdir.strpath) is None
