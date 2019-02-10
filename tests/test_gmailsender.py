import pytest

from emailer.gmailsender import GmailSender


@pytest.fixture
def gmail(stub):
  # https://developers.google.com/gmail/api/v1/reference/users/messages/send
  return stub(
      users=lambda: stub(
          messages=lambda: stub(
              send=lambda **kwargs: stub(
                  execute=lambda: kwargs))))


def test_send_message_uses_me_as_user_id(gmail):
  sender = GmailSender(gmail)
  assert sender.send('hi') == {
      'userId': 'me',
      'body': 'hi',
      }
