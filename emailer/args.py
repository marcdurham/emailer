import argparse
import os


def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config-dir', default=os.getcwd(),
                      help='Directory containing emailer.json file.')
  return parser


def get_options(args=None):
  return get_parser().parse_args(args)
