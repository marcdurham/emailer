import json
import os.path

import pytest

from emailer import config
from emailer.config import Config
from emailer.recipient import Recipient


def test_set_new_serialized_creds():
  assert Config('hi').set_serialized_creds('bye').serialized_creds == 'bye'


def test_load_none_file_raises_invalid_file_error():
  with pytest.raises(config.InvalidFileError, match='None'):
    config.load_from_file(None)


def test_load_nonexistent_file_raises_invalid_file_error(tmpdir):
  file_name = tmpdir.join('does_not_exist').strpath
  with pytest.raises(config.InvalidFileError, match=file_name):
    config.load_from_file(file_name)


def test_load_returns_filled_config_object(tmpdir):
  config_file = tmpdir.join('config.json')
  config_file.write(
      json.dumps({'client_secret': 's', 'serialized_creds': 'world'}))
  config_data = config.load_from_file(config_file.strpath)
  assert config_data.serialized_creds == 'world'
  assert config_data.client_secret == 's'


def test_load_empty_file_raises_invalid_file_content_error(tmpdir):
  with pytest.raises(config.InvalidFileError, match='config.json'):
    config_file = tmpdir.join('config.json')
    config_file.write('')
    config.load_from_file(config_file.strpath)


def test_validate_fails_without_valid_client_secret_config():
  with pytest.raises(config.InvalidFileError, match='client_secret'):
    config.Config().validate()


def test_get_keys_returns_only_unique_keys():
  assert Config(keys={'a': 1, 'b': 1}).get_keys(['a', 'b']) == {1}
  assert Config(keys={'a': 1, 'b': 1}).get_all_keys() == {1}


def test_get_keys_returns_no_keys_by_default_and_all_keys_if_passed():
  conf = Config(keys={'a': 1, 'b': 2})
  assert list(conf.get_keys([])) == []
  assert list(conf.get_keys(['a'])) == [1]
  assert list(conf.get_all_keys()) == [1, 2]


def test_get_extra_values_returns_extra_values_if_any():
  assert Config(extra_values=None).get_extra_values() == {}
  assert Config(extra_values={1: 2}).get_extra_values() == {1: 2}


def test_get_extra_recipients_for_group_returns_recipient_if_in_group():
  assert Config(extra_emails=None).get_extra_recipients_for_group('') == []
  assert (Config(extra_emails={'a': 'b'}).get_extra_recipients_for_group('')
          == [])
  assert (Config(extra_emails={'a': 'b'}).get_extra_recipients_for_group('a')
          == [Recipient('b')])


def test_save_updates_config_file_with_data(tmpdir):
  config_file = tmpdir.join('config.json')
  config_obj = config.Config(client_secret='hi')
  config_obj.save_to_file(config_file.strpath)
  assert json.loads(config_file.read())['client_secret'] == 'hi'


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
  config_file = tmpdir.join('.emailer.json')
  config_file.write('')
  assert config.find_config_file(config_file.strpath) == config_file.strpath


def test_find_returns_none_if_no_existing_config(tmpdir, monkeypatch):
  monkeypatch.setattr(os.path, 'expanduser', lambda _: tmpdir.strpath)
  assert config.find_config_file(tmpdir.strpath) is None
