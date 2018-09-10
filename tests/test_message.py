import base64
import email.message

from emailer.message import Message
from emailer.recipient import Recipient


def test_message_has_email_message_instance():
  assert isinstance(Message().email_message, email.message.EmailMessage)


def test_message_subject_is_in_email_message():
  assert Message(subject='Test').email_message['Subject'] == 'Test'


def test_message_recipient_replyto_is_in_email_message():
  sender = Recipient('sender')
  recipient = Recipient('to@example.com')
  replyto = Recipient('replyto@example.com')
  message = Message(sender=sender, recipient=recipient, replyto=replyto)
  assert message.email_message['From'] == sender.email
  assert message.email_message['To'] == recipient.email
  assert message.email_message['Reply-To'] == replyto.email


def test_message_body():
  message = Message(html_body='<h1>Hi</h1>')
  assert message.email_message.get_content() == '<h1>Hi</h1>\n'


def test_message_as_bytes_pass_through():
  message = Message(subject='Test', html_body='<h1>Hi</h1>')
  assert message.as_bytes() == message.email_message.as_bytes()


def test_message_gmail_api_body():
  message = Message(html_body='<h1>Hi</h1>')
  assert message.gmail_body == {
      'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
  }
