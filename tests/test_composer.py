from emailer import composer
from emailer.message import Message
from emailer.recipient import Recipient


def test_replace_replaces_names_with_values():
  assert composer.replace('{hi}', {'hi': 'bye'}) == 'bye'


def test_replace_leaves_undefined_template_names():
  assert composer.replace('{hi}', {}) == '{hi}'


def test_compose_email_body_replaces_shortcuts_and_markdown():
  body = composer.compose_email_body({
      'body': '{shortcut} {markdown} {context}',
      'context': 'c',
      }, {
      'shortcut': 's',
      }, {
      'markdown': 'm',
      })
  assert body == 's m c'


def test_compose_email_body_replaces_recursively():
  body = composer.compose_email_body({
      'body': '{shortcut}',
      'context': '{markdown-2}',
      }, {
      'shortcut': '{markdown}',
      }, {
      'markdown': '{context}',
      'markdown-2': 'c',
      })
  assert body == 'c'
