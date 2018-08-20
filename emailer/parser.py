from .recipient import Recipient


def parse_emails(data):
  res = dict()
  keys = data[0]
  defaults = data[1]
  def fill_defaults(vals):
    return [v if v != '' else d for v, d in zip(vals, defaults)]

  for row in data[2:]:
    values = fill_defaults(row)
    res[row[0]] = {k: v for k, v in zip(keys, values)}
  return res


def parse_recipients(data):
  res = []
  keys = data[0]
  for row in data[1:]:
    recipient = Recipient(row[0], row[1])
    recipient = recipient.add_highlight(recipient.name)
    for header, value in zip(keys[2:], row[2:]):
      if 'highlight' in header.lower():
        recipient = recipient.add_highlight(value)
      elif value != '':
        recipient = recipient.add_group(header.strip().lower())
    res.append(recipient)
  return res


def parse_general(data):
  # Ignore first row as header
  return {row[0]: row[1] for row in data[1:]}
