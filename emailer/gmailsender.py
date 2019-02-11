import base64


class GmailSender():
  '''Wraps the gmail sending API.'''

  def __init__(self, gmail):
    self.gmail = gmail

  def send(self, message):
    gmail_message = self.convert(message)
    return self.send_gmail_message(gmail_message)

  def send_gmail_message(self, message):
    return self.gmail.users().messages().send(
        userId='me', body=message).execute()

  @staticmethod
  def convert(msg):
    return {'raw': base64.urlsafe_b64encode(bytes(msg))}
