'''
Models for messages that are sent with servers.
'''

import email
import email.policy
import re
import smtplib
import time

import attr
import requests


@attr.s(frozen=True)
class Email():
  email = attr.ib(default='')

  @property
  def username(self):
    return self.email.split('@')[0]

  @property
  def domain(self):
    return self.email.split('@')[1]

  def is_valid(self):
    return self.email and re.match(r'.+@.+\..+', self.email)


@attr.s(frozen=True)
class Person():
  _name = attr.ib()
  _email = attr.ib(default='')
  _highlights = attr.ib(factory=list)

  @property
  def name(self):
    return self._name

  @property
  def email(self):
    return Email(self._email)

  @property
  def header_address(self):
    return email.headerregistry.Address(
        self._name, self.email.username, self.email.domain)

  def formatted(self):
    return '{} <{}>'.format(self._name, self._)


@attr.s(frozen=True)
class Message():
  sender = attr.ib()
  recipient = attr.ib()
  subject = attr.ib()
  html = attr.ib()
  reply_to = attr.ib(default=None)

  def get_message(self):
    message = email.message.EmailMessage(email.policy.SMTP)
    message['Subject'] = self.subject
    message['From'] = self.sender.header_address()
    message['To'] = self.recipient.header_address()
    if self.reply_to:
      message['Reply-To'] = self.reply_to.header_address()
    message.set_content(self.html, subtype='html', cte='quoted-printable')
    return message


@attr.s
class Server():
  '''SMTP Server, defaults to Gmail'''

  _user = attr.ib()
  _password = attr.ib()
  _host = attr.ib(default='smtp.gmail.com')
  _port = attr.ib(default=587)
  _skip_send = attr.ib(default=True)
  _SECONDS_BETWEEN_EMAILS = 0.1  # 100 ms

  def send(self, messages, verbose=False):
    with smtplib.SMTP(self._host, self._port) as server:
      server.starttls()
      server.login(self._user, self._password)
      for message in messages:
        html_message = message.get_email_message()
        if not self._skip_send:
          server.send_message(html_message)
          time.sleep(self._SECONDS_BETWEEN_EMAILS)
        if verbose:
          print('Sent mail to {}'.format(message.recipient.formatted()))


@attr.s
class MailGun():
  _host = attr.ib()
  _api_key = attr.ib()
  _skip_send = attr.ib()
  _API_V3 = 'https://api.mailgun.net/v3/{}/messages.mime'

  def send(self, messages):
    for message in messages:
      if not self._skip_send:
        requests.post(
            self._API_V3.format(self._host),
            auth=('api', self._api_key),
            data={'to': message.recipient.header_address()},
            files={'message': bytes(message.get_email_message())})
