import argparse
import datetime
import os

import pytest

from emailer import args, __version__


def test_get_version_returns_module_version():
  assert __version__ in args.get_version()


def test_sample_config_returns_config_file():
  assert 'keys' in args.get_sample_config()


def test_args_returns_argument_parser():
  assert isinstance(args.get_parser(), argparse.ArgumentParser)


def test_args_returns_default_namespace():
  assert isinstance(args.get_parsed_args([]), argparse.Namespace)


def test_args_defaults():
  options = args.get_parsed_args([])
  assert options.config_dir == os.getcwd()
  assert options.key_names is None
  assert options.date == datetime.date.today().isoformat()
  assert not options.verbose
  assert not options.sample_config
  assert not options.version
  assert not options.active
  assert not options.dryrun
  assert not options.test
  assert not options.all_keys
  assert not options.skip_send


def test_key_names_collects_values():
  assert args.get_parsed_args(['--key-names', 'a']).key_names == ['a']
  assert args.get_parsed_args(['-k', 'a']).key_names == ['a']
  assert args.get_parsed_args(
      ['--key-names', 'a', 'b']).key_names == ['a', 'b']
  assert args.get_parsed_args(['-k', 'a', 'b']).key_names == ['a', 'b']


def test_verbose_stores_true_if_passed():
  assert args.get_parsed_args(['--verbose']).verbose
  assert args.get_parsed_args(['-v']).verbose


def test_version_stores_true_if_passed():
  assert args.get_parsed_args(['--version']).version
  assert args.get_parsed_args(['-V']).version


def test_date_returns_date_if_passed():
  assert args.get_parsed_args(['--date', '2018-04-04']).date == '2018-04-04'


def test_each_group_can_be_set():
  assert args.get_parsed_args(['--active']).active
  assert args.get_parsed_args(['--dryrun']).dryrun
  assert args.get_parsed_args(['--test']).test


def test_only_one_group_can_be_set():
  with pytest.raises(SystemExit):
    args.get_parsed_args(['--active', '--dryrun'])
