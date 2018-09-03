import datetime
import itertools

from .recipient import Recipient


def _fill_defaults(values, defaults):
  return (v if v != '' else d
          for v, d in itertools.zip_longest(values, defaults, fillvalue=''))


def parse_emails(data):
  keys = data[0]
  defaults = data[1]
  for row in data[2:]:
    values = _fill_defaults(row, defaults)
    date = datetime.date.fromisoformat(row[0])
    yield date, {k: v for k, v in zip(keys, values)}


def parse_emails_for_date(data, target_date):
  for date, values in parse_emails(data):
    if date == target_date:
      yield values


def parse_recipients(data):
  keys = data[0]
  for row in data[1:]:
    highlights = []
    groups = []
    for header, value in zip(keys[1:], row[1:]):
      clean_header = header.strip().lower()
      clean_value = value.strip()
      if 'highlight' in clean_header and clean_value:
        highlights.append(clean_value)
      elif clean_value != '':
        groups.append(clean_header)
    yield Recipient(email=row[0],
                    highlights=tuple(highlights),
                    groups=tuple(groups))


def parse_recipients_in_group(data, group):
  return (r for r in parse_recipients(data) if r.in_group(group))


def parse_general(data):
  # Ignore first row as header
  if data is None:
    return {}
  return {row[0]: row[1] for row in data[1:]}
