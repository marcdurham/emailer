import logging
import sys

from . import shell
from .args import get_parsed_args, get_sample_config, get_version
from .options import Options


def main():
  options = Options(get_parsed_args())
  setup_logging(options.log_level)
  if options.version:
    print(get_version())
    return 0
  if options.sample_config:
    print(get_sample_config())
    return 0

  if not options.group:
    print('No group provided')
    return -1

  return shell.process(options)


def setup_logging(level):
  logging.basicConfig(level=level,
                      format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


def init():
  """allow 100% coverage by putting the __name__ check in a function"""
  if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

init()
