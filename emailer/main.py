import logging
import sys

from . import shell
from .args import get_parsed_args
from .options import Options

def main():
  options = Options(get_parsed_args())
  setup_logging(options.log_level)
  if options.version:
    print(options.get_version())
  elif options.sample_config:
    print(options.get_sample_config())
  elif options.group:
    shell.process_sheets(group=options.group,
                         config_dir=options.config_dir,
                         key_names=options.key_names,
                         all_keys=options.all_keys,
                         date=options.send_date,
                         skip=options.skip_send)
  else:
    print('No group / key combination provided')


def setup_logging(level):
  logging.basicConfig(stream=sys.stdout, level=level,
                      format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


if __name__ == '__main__':
  main()
