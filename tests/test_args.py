import argparse
import datetime
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
  assert options.date == datetime.date.today()
