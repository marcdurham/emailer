from .recipient import Recipient


def _fill_defaults(values, defaults):
  return [v if v != '' else d for v, d in zip(values, defaults)]


def parse_emails(data):
  res = dict()
  keys = data[0]
  defaults = data[1]
  for row in data[2:]:
    values = _fill_defaults(row, defaults)
    res[row[0]] = {k: v for k, v in zip(keys, values)}
  return res


def parse_recipients(data):
  res = []
  keys = data[0]
  for row in data[1:]:
    recipient = Recipient(row[0], row[1])
    for header, value in zip(keys[2:], row[2:]):
      clean_header = header.strip().lower()
      if 'highlight' in clean_header:
        recipient = recipient.add_highlight(value)
      elif value != '':
        recipient = recipient.add_group(clean_header)
    res.append(recipient)
  return res


def parse_general(data):
  # Ignore first row as header
  if data is None:
    return {}
  return {row[0]: row[1] for row in data[1:]}
