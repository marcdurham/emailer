from emailer.recipient import Recipient


def test_recipient_default_empty_highlight_and_group():
  assert Recipient().highlights == ()
  assert Recipient().groups == ()
