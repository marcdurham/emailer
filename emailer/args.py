import argparse
import datetime
import logging
import os
from importlib import resources

import emailer


class Options():
  def __init__(self, options):
    self.options = options

  @property
  def log_level(self):
    if self.verbose:
      return logging.INFO
    return logging.WARNING

  @property
  def group(self):
    if self.active:
      return 'active'
    if self.dryrun:
      return 'dryrun'
    if self.test:
      return 'test'
    return None

  @property
  def send_date(self):
    if self.group == 'dryrun':
      date = datetime.date.fromisoformat(self.date)
      return (date + datetime.timedelta(days=1)).isoformat()
    return self.date

  def __getattr__(self, name):
    '''Pass through implicit attributes.'''
    if hasattr(self.options, name):
      return getattr(self.options, name)
    return None

  @staticmethod
  def get_version():
    return f'{emailer.__version__}'

  @staticmethod
  def get_sample_config():
    return resources.read_text(emailer, 'sample-emailer.json')


def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config-dir', default=os.getcwd(),
                      help='Directory containing config file. Default is '
                           'current working directory.')
  parser.add_argument('-k', '--key-names', nargs='*',
                      help='Key name(s) matching key(s) in the config.')
  parser.add_argument('--all-keys', action='store_true',
                      help='Run for all available keys in config.')
  parser.add_argument('-d', '--date', default=datetime.date.today().isoformat(),
                      help='Date for which to send emails (YYYY-MM-DD). The '
                           'default is today.')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='Display more logging output')
  parser.add_argument('-V', '--version', action='store_true',
                      help='Print the current emailer module version and exit.')
  parser.add_argument('--sample-config', action='store_true',
                      help='Print a sample config. Save as emailer.json or '
                           '.emailer.json and exit.')
  parser.add_argument('--skip-send', action='store_true',
                      help='Avoid actually sending emails, useful for testing.')
  # Only one group can be specified per-run.
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--active', action='store_true',
                     help='Send emails to all active recipients.')
  group.add_argument('--dryrun', action='store_true',
                     help='Send emails one day early to dryrun recipients.')
  group.add_argument('--test', action='store_true',
                     help='Send emails only to test recipients.')
  return parser


def get_parsed_args(argv=None):
  return get_parser().parse_args(argv)
