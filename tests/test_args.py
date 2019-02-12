import argparse
import datetime
import logging
import os

import pytest

from emailer import args, __version__
from emailer.args import Options


class TestOptions():
  def test_returns_cmdline_value_if_no_method_defined(self, stub):
    options = Options(stub(a='hello'))
    assert options.a == 'hello'

  def test_group_yields_whichever_group_is_passed(self, stub):
    assert Options(stub(active=1)).group == 'active'
    assert Options(stub(dryrun=1)).group == 'dryrun'
    assert Options(stub(test=1)).group == 'test'
    assert Options(stub()).group is None # Perhaps an exception is better here.

  def test_send_date_is_the_same_as_date(self, stub):
    options = Options(stub(date='2018-04-05', active=1))
    assert options.send_date == '2018-04-05'

  def test_get_date_returns_one_day_later_for_dryrun_group(self, stub):
    options = Options(stub(date='2018-04-05', dryrun=1))
    assert options.send_date == '2018-04-06'

  def test_log_level_returns_info_for_verbose_warn_by_default(self, stub):
    assert Options(stub(verbose=True)).log_level == logging.INFO
    assert Options(stub()).log_level == logging.WARNING

  def test_get_version_returns_module_version(self):
    assert __version__ in Options.get_version()

  def test_sample_config_returns_config_file(self):
    assert 'keys' in Options.get_sample_config()


class TestParsedArgs():
  def test_args_returns_argument_parser(self):
    assert isinstance(args.get_parser(), argparse.ArgumentParser)

  def test_args_returns_default_namespace(self):
    assert isinstance(args.get_parsed_args([]), argparse.Namespace)

  def test_args_defaults(self):
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

  def test_key_names_collects_values(self):
    assert args.get_parsed_args(['--key-names', 'a']).key_names == ['a']
    assert args.get_parsed_args(['-k', 'a']).key_names == ['a']
    assert args.get_parsed_args(
        ['--key-names', 'a', 'b']).key_names == ['a', 'b']
    assert args.get_parsed_args(['-k', 'a', 'b']).key_names == ['a', 'b']

  def test_verbose_stores_true_if_passed(self):
    assert args.get_parsed_args(['--verbose']).verbose
    assert args.get_parsed_args(['-v']).verbose

  def test_version_stores_true_if_passed(self):
    assert args.get_parsed_args(['--version']).version
    assert args.get_parsed_args(['-V']).version

  def test_date_returns_date_if_passed(self):
    assert args.get_parsed_args(['--date', '2018-04-04']).date == '2018-04-04'

  def test_each_group_can_be_set(self):
    assert args.get_parsed_args(['--active']).active
    assert args.get_parsed_args(['--dryrun']).dryrun
    assert args.get_parsed_args(['--test']).test

  def test_only_one_group_can_be_set(self):
    with pytest.raises(SystemExit):
      args.get_parsed_args(['--active', '--dryrun'])
