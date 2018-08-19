import email.headerregistry

from emailer.recipient import Recipient


def test_recipient_default_empty_highlight_and_group():
  assert Recipient().highlights == ()
  assert Recipient().groups == ()


def test_recipient_add_highlight():
  assert Recipient().add_highlight('Me').highlights == ('Me',)


def test_recipient_add_group():
  assert Recipient().add_group('Me').groups == ('Me',)


def test_recipient_default_not_active_dryrun_test():
  assert not Recipient().is_active()
  assert not Recipient().is_dryrun()
  assert not Recipient().is_test()


def test_recipient_email_header():
  assert Recipient('Daniel', 'daniel@example.com').header == (
      email.headerregistry.Address('Daniel', 'daniel', 'example.com'))
