import argparse
import datetime
import logging
import os

from emailer import args


def test_args_returns_argument_parser_instance():
  assert isinstance(args.get_parser(), argparse.ArgumentParser)


def test_args_returns_default_options_with_no_args():
  options = args.get_options([])
  assert isinstance(options, argparse.Namespace)


def test_args_defaults():
  options = args.get_options([])
  assert options.config_dir == os.getcwd()
  assert options.key_names == None
  assert options.date == None
  assert options.verbose == False


def test_key_names_collects_values():
  assert args.get_options(['--key-name', 'a']).key_names == ['a']
  assert args.get_options(['-k', 'a']).key_names == ['a']
  assert args.get_options(
      ['--key-name', 'a', '-k', 'b']).key_names == ['a', 'b']


def test_verbose_stores_true_if_passed():
  assert args.get_options(['--verbose']).verbose == True
  assert args.get_options(['-v']).verbose == True


def test_get_date_parses_date_to_datetime_value_and_today_by_default(stub):
  assert args.get_date(stub(date=None)) == datetime.date.today()
  assert args.get_date(stub(date='2018-05-12')) == datetime.date(2018, 5, 12)


def test_get_log_level_returns_info_for_verbose_and_warning_by_default(stub):
  assert args.get_log_level(stub(verbose=True)) == logging.INFO
  assert args.get_log_level(stub(verbose=False)) == logging.WARNING
