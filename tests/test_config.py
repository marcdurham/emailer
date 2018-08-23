import json

import pytest

from emailer import config


def test_load_none_file_returns_empty_dict():
  assert config.load(None) == {}


def test_load_nonexistent_file_returns_empty_dict(tmpdir):
  config_file = tmpdir.join('does_not_exist')
  assert config.load(config_file) == {}


def test_load_returns_json_file_contents(tmpdir):
  config_file = tmpdir.join('config.json')
  json.dump({'hi': 'bye'}, config_file.open('w'))
  assert config.load(config_file.strpath) == {'hi': 'bye'}


def test_load_empty_file_returns_empty_dict(tmpdir):
  config_file = tmpdir.join('config.json')
  config_file.write('')
  assert config.load(config_file.strpath) == {}


# TODO: Add tests for save function
