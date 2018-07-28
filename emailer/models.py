'''
Models for messages that are sent with servers.
'''

# TODO: Rename all other email instances
import email as email_package
# TODO: Avoid specific imports
from email import policy
import re
import smtplib
import time

import requests


class Person():
  '''The combination of a full name and an email address.'''

  def __init__(self, *, name, email):
    self.name = name
    self.email = email
    if email:
      self.username, self.domain = email.split('@')
    self.highlights = [self.name]

  @classmethod
  def create(cls, attr_list):
    name, email = attr_list
    return cls(name=name, email=email)

  def has_valid_email(self):
    if self.email and re.match(r'.+@.+\..+', self.email):
      return True
    return False

  def get_address(self):
    return email_package.headerregistry.Address(
        self.name, self.username, self.domain)

  def __repr__(self):
    return '{name} <{email}>'.format(name=self.name, email=self.email)


class Message():
  def __init__(self, *, sender=None, recipient=None, reply_to=None,
               subject=None, html=None):
    self.sender = sender
    self.recipient = recipient
    self.reply_to = reply_to
    self.subject = subject
    self.html = html

  def get_message(self):
    message = email_package.message.EmailMessage(policy.SMTP)
    message['Subject'] = self.subject
    message['From'] = self.sender.get_address()
    message['To'] = self.recipient.get_address()
    if self.reply_to:
      message['Reply-To'] = self.reply_to.get_address()
    message.set_content(self.html, subtype='html', cte='quoted-printable')
    return message


class Server():
  SECONDS_BETWEEN_EMAILS = 1
  def __init__(self, *, host, port, user, password, skip_send):
    self.host = host
    self.port = port
    self.user = user
    self.password = password
    self.skip_send = skip_send

  def send(self, messages, verbose=False):
    server = smtplib.SMTP(self.host, self.port)
    if self.user and self.password:
      server.starttls()
      server.login(self.user, self.password)
    for message in messages:
      html_message = message.get_message()
      if not self.skip_send:
        server.send_message(html_message)
        time.sleep(self.SECONDS_BETWEEN_EMAILS)
      if verbose:
        print('Sent mail to {}'.format(message.recipient))
    server.quit()


class Gmail(Server):
  '''Simple to use, simply supply user and password of any gmail account.'''
  def __init__(self, *, user, password, skip_send):
    super().__init__(host='smtp.gmail.com', port=587, user=user,
                     password=password, skip_send=skip_send)


class MailGun():
  API_V3 = 'https://api.mailgun.net/v3/{}/messages.mime'

  def __init__(self, *, host, api_key, skip_send):
    self.host = host
    self.api_key = api_key
    self.skip_send = skip_send

  def send(self, messages):
    for message in messages:
      if not self.skip_send:
        requests.post(
            self.API_V3.format(self.host),
            auth=('api', self.api_key),
            data={'to': message.recipient.get_address()},
            files={'message': bytes(message.get_message())})
