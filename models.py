'''
Models for messages that are sent with servers.
'''

import re
import smtplib
from email.mime import multipart
from email.mime import text


CHARSET = 'UTF-8'


class Person(object):
    '''The combination of a full name and an email address.'''

    def __init__(self, *, name, email):
        self.name = name
        self.email = email

    @classmethod
    def create(cls, attr_list):
        name, email = attr_list
        return cls(name=name, email=email)

    def has_valid_email(self):
        if self.email and re.match(r'.+@.+\..+', self.email):
            return True
        return False

    def __str__(self):
        return '{name} <{email}>'.format(name=self.name, email=self.email)


class Message(object):
    def __init__(self, *, sender=None, recipient=None, reply_to=None,
                 subject=None, text=None, html=None, charset=CHARSET):
        self.sender = sender
        self.recipient = recipient
        self.reply_to = reply_to
        self.subject = subject
        self.text = text
        self.html = html
        self.charset = charset

    def __str__(self):
        body = multipart.MIMEMultipart('alternative')
        if self.text:
            body.attach(text.MIMEText(self.text, 'plain', self.charset))
        if self.html:
            body.attach(text.MIMEText(self.html, 'html', self.charset))
        body['from'] = str(self.sender)
        body['reply-to'] = str(self.reply_to)
        body['to'] = str(self.recipient)
        body['subject'] = self.subject
        return str(body)


class Server(object):
    def __init__(self, *, host, port, use_tls, user, password):
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.user = user
        self.password = password

    def send(self, messages):
        server = smtplib.SMTP(self.host, self.port)
        if self.user and self.password:
            if self.use_tls:
                server.ehlo()
                server.starttls()
                server.ehlo()
            server.login(self.user, self.password)
        for message in messages:
            server.sendmail(
                    message.sender.email,
                    message.recipient.email,
                    str(message))
        server.quit()


class Gmail(Server):
    '''Simple to use, simply supply user and password of any gmail account.'''
    def __init__(self, *, user, password):
        super().__init__(host='smtp.gmail.com', port=587, use_tls=True,
                         user=user, password=password)

