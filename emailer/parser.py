import datetime
import itertools

from .recipient import Recipient


# TODO: Refactor
def parse_emails(data):
  # Only add emails with send-date filled in, minus name and default columns
  num_emails = len(data[0]) - 2
  if num_emails <= 0:
    return
  emails = [dict() for _ in range(num_emails)]
  for row in data:
    name = row[0]
    if len(row) >= 2:
      default = row[1]
    else:
      default = ''
    for email, value in itertools.zip_longest(emails, row[2:]):
      if value:
        email[name] = value
      else:
        email[name] = default
  for email in emails:
    date = datetime.date.fromisoformat(email['send-date'])
    yield date, email


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
