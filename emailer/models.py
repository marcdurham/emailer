'''
Models for messages that are sent with servers.
'''

import email.headerregistry
import email.message
import email.policy
import re
import requests
import time


class Person(object):
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
        return email.headerregistry.Address(
                self.name, self.username, self.domain)

    def __repr__(self):
        return '{name} <{email}>'.format(name=self.name, email=self.email)


class Message(object):
    def __init__(self, *, sender=None, recipient=None, reply_to=None,
                 subject=None, text=None, html=None):
        self.sender = sender
        self.recipient = recipient
        self.reply_to = reply_to
        self.subject = subject
        self.text = text
        self.html = html

    def get_message(self):
        message = email.message.EmailMessage(email.policy.SMTP)
        message['Subject'] = self.subject
        message['From'] = self.sender.get_address()
        message['To'] = self.recipient.get_address()
        if self.reply_to:
            message['Reply-To'] = self.reply_to.get_address()
        message.set_content(self.html, subtype='html', cte='quoted-printable');
        return message


class MailGun(object):
    API_V3 = 'https://api.mailgun.net/v3/{}/messages.mime'

    def __init__(self, *, host, api_key):
        self.host = host
        self.api_key = api_key

    def send(self, messages):
        for message in messages:
            requests.post(
                    self.API_V3.format(self.host),
                    auth=('api', self.api_key),
                    data={'to': message.recipient.get_address()},
                    files={'message': bytes(message.get_message())})

