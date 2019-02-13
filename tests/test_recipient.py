from emailer.recipient import Recipient


def test_empty_highlight_and_group_by_default():
  assert Recipient().highlights == ()
  assert Recipient().groups == ()


def test_valid_only_when_email_is_valid():
  assert not Recipient(email='').is_valid()
  assert Recipient(email='a@example.com').is_valid()
