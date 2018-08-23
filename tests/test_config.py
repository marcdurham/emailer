import json
import os.path

import pytest

from emailer import config


def test_load_none_file_raises_invalid_file_error():
  with pytest.raises(config.InvalidFileError, match='None'):
    config.load(None)


def test_load_nonexistent_file_raises_invalid_file_error(tmpdir):
  file_name = tmpdir.join('does_not_exist').strpath
  with pytest.raises(config.InvalidFileError, match=file_name):
    config.load(file_name)


def test_load_returns_json_file_contents(tmpdir):
  config_file = tmpdir.join('config.json')
  config_file.write(json.dumps({'hi': 'bye'}))
  assert config.load(config_file.strpath) == {'hi': 'bye'}


def test_load_empty_file_raises_invalid_file_content_error(tmpdir):
  with pytest.raises(config.InvalidFileContentError, match='config.json'):
    config_file = tmpdir.join('config.json')
    config_file.write('')
    config.load(config_file.strpath)


def test_load_bad_json_file_raises_invalid_file_content_error(tmpdir):
  with pytest.raises(config.InvalidFileContentError, match='config.json'):
    config_file = tmpdir.join('config.json')
    config_file.write('badjson')
    config.load(config_file.strpath)


def test_validate_fails_without_valid_client_secret_config():
  with pytest.raises(config.InvalidFileContentError, match='client_secret'):
    config.validate({})


def test_save_updates_config_file_with_data(tmpdir):
  config_file = tmpdir.join('config.json')
  config.save(config_file.strpath, {'hi': 'bye'})
  assert json.loads(config_file.read()) == {'hi': 'bye'}


def test_dirs_yields_all_possible_names():
  assert list(config.dirs('/test/one')) == [
      '/test/one/.emailer/config.json',
      '/test/.emailer/config.json',
      '/.emailer/config.json',
      os.path.expanduser('~/.emailer/config.json'),
      ]


def test_find_returns_first_existing_config(tmpdir):
  config_file = tmpdir.mkdir('.emailer').join('config.json')
  config_file.write('')
  assert config.find(config_file.strpath) == config_file.strpath


def test_find_returns_none_if_no_existing_config(tmpdir, monkeypatch):
  monkeypatch.setattr(os.path, 'expanduser', lambda _: tmpdir.strpath)
  assert config.find(tmpdir.strpath) is None


def test_find_returns_home_dir_if_no_existing_config(tmpdir, monkeypatch):
  hi_dir = tmpdir.mkdir('hi')
  config_file = hi_dir.mkdir('.emailer').join('config.json')
  config_file.write('')
  monkeypatch.setattr(os.path, 'expanduser', lambda _: hi_dir.strpath)
  assert config.find(tmpdir.strpath) == config_file.strpath
