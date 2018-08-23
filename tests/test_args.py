import argparse

from emailer import args


def test_parser_returns_argument_parser_instance():
  assert isinstance(args.parser(), argparse.ArgumentParser)
