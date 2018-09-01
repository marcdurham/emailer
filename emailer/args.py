import argparse
import datetime
import logging
import os


def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config-dir', default=os.getcwd(),
                      help='Directory containing configfile. Default is '
                           'current working directory.')
  parser.add_argument('-k', '--key-name', action='append', dest='key_names',
                      help='Key name matching a key in the config. Default '
                           'is all available key names.')
  parser.add_argument('-d', '--date',
                      help='Date for which to send emails (YYYY-MM-DD). The '
                           'default is today.')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='Display more logging output')
  return parser


def get_options(args=None):
  return get_parser().parse_args(args)


def get_date(options):
  if options.date:
    return datetime.date.fromisoformat(options.date)
  return datetime.date.today()


def get_log_level(options):
  if options.verbose:
    return logging.INFO
  return logging.WARNING
