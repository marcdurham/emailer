from emailer.emailvalidator import is_email_valid


def test_well_formed_email_is_valid():
  assert is_email_valid('a@example.com')


def test_email_without_at_sign_is_invalid():
  assert not is_email_valid('a')


def test_email_without_name_is_invalid():
  assert not is_email_valid('@example.com')


def test_email_without_domain_is_invalid():
  assert not is_email_valid('a@')


def test_email_without_top_level_domain_is_invalid():
  assert not is_email_valid('a@example')
