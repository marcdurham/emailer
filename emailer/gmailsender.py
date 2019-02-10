import logging


class GmailSender(object):
  '''Wraps the gmail sending API.'''

  def __init__(self, gmail):
    self.gmail = gmail

  def send(self, message):
    logging.info('Sending %s', message)
    return self.gmail.users().messages().send(
        userId='me', body=message).execute()
