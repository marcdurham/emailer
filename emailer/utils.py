'''
Various standalone utility functions
'''

import dateutil.parser


def parse_date(date_string):
  return dateutil.parser.parse(date_string).date()


def merge_with_default(d, default):
  return {k: default[k] if v is None else v
          for k, v in d.items()}


def newline_to_br(d):
  return {k: v.replace('\n', '<br>') if isinstance(v, str) else v
          for k, v in d.items()}
