import itertools

from .recipient import Recipient
from .name import DATE


def transpose(lists):
  return (vals for vals in itertools.zip_longest(*lists, fillvalue=''))


def parse_emails(original_data):
  data = transpose(original_data)
  keys = next(data, '')
  defaults = next(data, '')
  for row in data:
    yield {k: r if r else d for k, r, d in zip(keys, row, defaults)}


def parse_emails_for_date(data, target_date):
  for email in parse_emails(data):
    if email[DATE] == target_date:
      yield email


def parse_recipients(data):
  keys = data[0]
  for row in data[1:]:
    email = row[0]
    highlights = []
    groups = []
    for header, value in zip(keys[1:], row[1:]):
      clean_header = header.strip().lower()
      clean_value = value.strip()
      if 'highlight' in clean_header and clean_value:
        highlights.append(clean_value)
      elif clean_value != '':
        groups.append(clean_header)
    yield Recipient(email=email,
                    highlights=tuple(highlights),
                    groups=tuple(groups))


def parse_recipients_in_group(data, group):
  return (r for r in parse_recipients(data) if r.in_group(group))
