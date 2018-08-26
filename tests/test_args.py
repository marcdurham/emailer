import argparse
import os

from emailer import args


def test_parser_returns_argument_parser_instance():
  assert isinstance(args.get_parser(), argparse.ArgumentParser)


def test_parser_returns_default_options_with_no_args():
  options = args.get_options([])
  assert isinstance(options, argparse.Namespace)


def test_parser_default_config_dir_is_current_working_dir():
  assert args.get_options([]).config_dir == os.getcwd()
