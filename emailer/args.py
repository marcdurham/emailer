import argparse
import datetime
import os


def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config-dir', default=os.getcwd(),
                      help='Directory containing configfile.')
  parser.add_argument('-k', '--key-name', nargs='*', dest='key_names',
                      help='Key name matching a key in the config.')
  parser.add_argument('-d', '--date', default=datetime.date.today(),
                      help='Date for which to send emails')
  return parser


def get_options(args=None):
  return get_parser().parse_args(args)
