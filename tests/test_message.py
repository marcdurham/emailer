import email.message

from emailer.message import Message
from emailer.recipient import Recipient


def test_message_has_email_message_instance():
  assert isinstance(Message().email_message, email.message.EmailMessage)


def test_message_subject_is_in_email_message():
  assert Message(subject='Test').email_message['Subject'] == 'Test'


def test_message_sender_recipient_replyto_is_in_email_message():
  sender = Recipient('Sender', 'sender@example.com')
  recipient = Recipient('To', 'to@example.com')
  replyto = Recipient('Reply', 'replyto@example.com')
  message = Message(sender=sender, recipient=recipient, replyto=replyto)
  assert message.email_message['From'] == str(sender.header)
  assert message.email_message['To'] == str(recipient.header)
  assert message.email_message['Reply-To'] == str(replyto.header)


def test_message_body():
  message = Message(body='<h1>Hi</h1>')
  assert message.email_message.get_content() == '<h1>Hi</h1>\n'
