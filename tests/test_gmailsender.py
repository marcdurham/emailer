import base64

import pytest

from emailer.gmailsender import GmailSender


@pytest.fixture
def gmail(stub):
  # https://developers.google.com/gmail/api/v1/reference/users/messages/send
  return stub(users=lambda: stub(messages=lambda: stub(
      send=lambda **kwargs: stub(execute=lambda: kwargs))))


def test_send_converts_message_before_sending(gmail):
  sender = GmailSender(gmail)
  assert 'raw' in sender.send(b'hi')['body']


def test_send_gmail_message_uses_me_as_user_id(gmail):
  sender = GmailSender(gmail)
  assert sender.send_gmail_message('hi') == {'userId': 'me', 'body': 'hi'}


def test_convert_converts_messages_to_gmail_body():
  converted = GmailSender.convert(b'hi')
  assert converted == {'raw': base64.urlsafe_b64encode(b'hi').decode()}
