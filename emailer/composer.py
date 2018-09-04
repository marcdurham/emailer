from string import Template

import mistune

from .recipient import Recipient


def replace(text, values):
  return Template(text).safe_substitute(values)


def recursively_replace(text, values):
  current_text = text
  last_text = None
  while current_text != last_text:
    last_text = current_text
    current_text = replace(current_text, values)
  return current_text


def substitute_for_key(key, values):
  return recursively_replace(values.get(key, ''), values)


def replace_values(values):
  return {k: values.get(v, v) for k, v in values.items()}


def markdown(text):
  # Convert newlines to <br> with hard_wrap=True
  return mistune.markdown(text, hard_wrap=True)


def mark_text(text, highlights, values):
  for highlight in highlights:
    mark = values.get(highlight, highlight)
    text = text.replace(mark, f'<mark>{mark}</mark>')
  return text


def get_prefix_for_group(group):
  if group == 'dryrun':
    return '[DRYRUN] '
  if group == 'test':
    return '[TEST] '
  return ''


def get_replyto(values):
  replyto_email = values.get('replyto')
  if replyto_email:
    return Recipient(replyto_email)
  return None
