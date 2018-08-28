from emailer import parser
from emailer.recipient import Recipient


def test_parse_emails_with_default():
  res = parser.parse_emails([
      ['send-date', 'email-content'],
      ['', 'hi'],  # Defaults
      ['2018-01-01', ''],
  ])
  assert res == {
      '2018-01-01': {
          'send-date': '2018-01-01',
          'email-content': 'hi',
      },
  }


def test_parse_recipients_returns_list_of_recipients_no_default_values():
  res = parser.parse_recipients([
      ['Name', 'Email'],
      ['Daniel', 'daniel@example.com'],
  ])
  for recipient in res:
    assert isinstance(recipient, Recipient)
    assert recipient.groups == ()
    assert recipient.highlights == ()


def test_parse_recipients_case_insensitive_highlights():
  res = parser.parse_recipients([
      ['Name', 'Email', 'Highlight'],
      ['Daniel', 'daniel@example.com', 'Hi'],
  ])
  assert res[0].highlights == ('Hi',)


def test_parse_recipients_lower_case_groups():
  res = parser.parse_recipients([
      ['Name', 'Email', 'Active'],
      ['Daniel', 'daniel@example.com', 'X'],
  ])
  assert res[0].groups == ('active',)


def test_parse_recipients_skip_empty_groups():
  res = parser.parse_recipients([
      ['Name', 'Email', 'Active'],
      ['Daniel', 'daniel@example.com', ''],
  ])
  assert res[0].groups == ()


def test_parse_general_returns_generic_dict():
  res = parser.parse_general([
      ['Name', 'Value'],
      ['reply-to', 'Daniel'],
  ])
  assert res == {'reply-to': 'Daniel'}
