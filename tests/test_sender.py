import pytest
from pretend import stub

from emailer import sender


@pytest.fixture
def gmail():
  # https://developers.google.com/gmail/api/v1/reference/users/messages/send
  return stub(
      users=lambda: stub(
          messages=lambda: stub(
              send=lambda userId, body: stub(
                  execute=lambda: (userId, body)))))


def test_send_message_calls_correct_api(gmail):
  message = stub(gmail_body=5)
  assert sender.send_message(message, gmail) == ('me', 5)


def test_send_messages_sends_all_messages(gmail):
  messages = [stub(gmail_body=n) for n in range(5)]
  assert sender.send_messages(messages, gmail) == [('me', n) for n in range(5)]
