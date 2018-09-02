import datetime

from .recipient import Recipient


def _fill_defaults(values, defaults):
  return [v if v != '' else d for v, d in zip(values, defaults)]


def parse_emails(data):
  res = dict()
  keys = data[0]
  defaults = data[1]
  for row in data[2:]:
    values = _fill_defaults(row, defaults)
    date = datetime.date.fromisoformat(row[0])
    res[date] = {k: v for k, v in zip(keys, values)}
  return res


def parse_emails_for_date(data, date):
  parsed_data = parse_emails(data)
  if date in parsed_data:
    yield parsed_data[date]


def parse_recipients(data):
  keys = data[0]
  for row in data[1:]:
    highlights = []
    groups = []
    for header, value in zip(keys[2:], row[2:]):
      clean_header = header.strip().lower()
      clean_value = value.strip()
      if 'highlight' in clean_header and clean_value:
        highlights.append(clean_value)
      elif clean_value != '':
        groups.append(clean_header)
    yield Recipient(name=row[0],
                    email=row[1],
                    highlights=tuple(highlights),
                    groups=tuple(groups))


def parse_recipients_in_group(data, group):
  return (r for r in parse_recipients(data) if r.in_group(group))


def parse_general(data):
  # Ignore first row as header
  if data is None:
    return {}
  return {row[0]: row[1] for row in data[1:]}
