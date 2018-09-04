import argparse
import datetime
import logging
import os
import sys

from . import __version__


def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config-dir', default=os.getcwd(),
                      help='Directory containing config file. Default is '
                           'current working directory.')
  parser.add_argument('-k', '--key-name', action='append', dest='key_names',
                      help='Key name matching a key in the config. Default '
                           'is all available key names.')
  parser.add_argument('-d', '--date', default=datetime.date.today().isoformat(),
                      help='Date for which to send emails (YYYY-MM-DD). The '
                           'default is today.')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='Display more logging output')
  parser.add_argument('-V', '--version', action='store_true',
                      help='Print the current emailer module version.')
  parser.add_argument('--active', action='store_true',
                      help='Send emails to all active recipients.')
  parser.add_argument('--dryrun', action='store_true',
                      help='Send emails one day early to dryrun recipients.')
  parser.add_argument('--test', action='store_true',
                      help='Send emails only to test recipients.')
  return parser


def get_options(argv=None):
  return get_parser().parse_args(argv)


def get_log_level(options):
  if options.verbose:
    return logging.INFO
  return logging.WARNING


def get_groups(options):
  if options.active:
    yield 'active'
  if options.dryrun:
    yield 'dryrun'
  if options.test:
    yield 'test'


def get_date(options, group):
  if group == 'dryrun':
    date = datetime.date.fromisoformat(options.date)
    return (date - datetime.timedelta(days=1)).isoformat()
  return options.date


def print_version(options):
  if options.version:
    return sys.stdout.write(f'{__version__}\n')
  return None
