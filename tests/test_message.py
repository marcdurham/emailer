from email.message import EmailMessage

from emailer.message import Message
from emailer.recipient import Recipient


def test_message_has_email_message():
  assert isinstance(Message().email_message, EmailMessage)


def test_message_fields_are_in_email_message():
  sender = Recipient('sender')
  recipient = Recipient('to@example.com')
  replyto = Recipient('replyto@example.com')
  message = Message(subject='Hi',
                    sender=sender,
                    recipient=recipient,
                    replyto=replyto)
  assert message.email_message.items() == [
      ('Subject', 'Hi'),
      ('From', sender.email),
      ('To', recipient.email),
      ('Reply-To', replyto.email),
      ('Content-Type', 'text/html; charset="utf-8"'),
      ('Content-Transfer-Encoding', 'quoted-printable'),
      ('MIME-Version', '1.0'),
  ]


def test_message_body_is_email_message_content():
  message = Message(html_body='<h1>Hi</h1>\n')
  assert message.email_message.get_content() == '<h1>Hi</h1>\n'


def test_message_bytes_pass_through_to_email_message_as_bytes():
  message = Message()
  assert bytes(message) == message.email_message.as_bytes()
