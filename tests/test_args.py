import argparse
import datetime
import logging
import os
import sys

from emailer import args, __version__


def test_args_returns_argument_parser_instance():
  assert isinstance(args.get_parser(), argparse.ArgumentParser)


def test_args_returns_default_options_with_no_args():
  options = args.get_options([])
  assert isinstance(options, argparse.Namespace)


def test_args_defaults():
  options = args.get_options([])
  assert options.config_dir == os.getcwd()
  assert options.key_names is None
  assert options.date == datetime.date.today().isoformat()
  assert not options.verbose
  assert not options.version
  assert not options.active
  assert not options.dryrun
  assert not options.test


def test_key_names_collects_values():
  assert args.get_options(['--key-name', 'a']).key_names == ['a']
  assert args.get_options(['-k', 'a']).key_names == ['a']
  assert args.get_options(
      ['--key-name', 'a', '-k', 'b']).key_names == ['a', 'b']


def test_verbose_stores_true_if_passed():
  assert args.get_options(['--verbose']).verbose
  assert args.get_options(['-v']).verbose


def test_version_stores_true_if_passed():
  assert args.get_options(['--version']).version
  assert args.get_options(['-V']).version


def test_date_returns_date_if_valid():
  assert args.get_options(['--date', '2018-04-04']).date == '2018-04-04'


def test_get_date_returns_one_day_earlier_for_dryrun_group(stub):
  assert args.get_date(stub(date='2018-04-05'), 'dryrun') == '2018-04-04'
  assert args.get_date(stub(date='2018-04-05'), 'not') == '2018-04-05'


def test_get_groups_collects_groups():
  assert list(args.get_groups(args.get_options(['--active']))) == ['active']
  assert list(args.get_groups(args.get_options(
      ['--active', '--dryrun', '--test']))) == ['active', 'dryrun', 'test']


def test_get_log_level_returns_info_for_verbose_and_warning_by_default(stub):
  assert args.get_log_level(stub(verbose=True)) == logging.INFO
  assert args.get_log_level(stub(verbose=False)) == logging.WARNING


def test_print_version_calls_print_with_version(monkeypatch, stub):
  monkeypatch.setattr(sys.stdout, 'write', lambda x: x)
  assert args.print_version(stub(version=True)) == f'{__version__}\n'
  assert args.print_version(stub(version=False)) is None