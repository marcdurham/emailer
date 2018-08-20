'''
Models for messages that are sent with servers.
'''

import email
import email.policy
import re
import smtplib
import time

import attr


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
