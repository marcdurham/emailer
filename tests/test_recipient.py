import email.headerregistry

from emailer.recipient import Recipient


def test_recipient_default_empty_highlight_and_group():
  assert Recipient().highlights == ()
  assert Recipient().groups == ()


def test_recipient_in_group_if_and_only_if_in():
  recipient = Recipient(groups=('Hi',))
  assert recipient.in_group('Hi')
  assert not recipient.in_group('Other')


def test_recipient_email_header():
  assert Recipient('daniel@example.com').header == (
      email.headerregistry.Address(addr_spec='daniel@example.com'))
