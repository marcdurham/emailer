import dataclasses
import email.message

from .recipient import Recipient


@dataclasses.dataclass(frozen=True)
class Message():
  subject: str = ''
  sender: Recipient = None
  recipient: Recipient = None
  replyto: Recipient = None
  html_body: str = ''

  @property
  def email_message(self):
    message = email.message.EmailMessage()
    message['Subject'] = self.subject
    if self.sender:
      message['From'] = self.sender.email
    if self.recipient:
      message['To'] = self.recipient.email
    if self.replyto:
      message['Reply-To'] = self.replyto.email
    # CTE: https://en.wikipedia.org/wiki/MIME#Content-Transfer-Encoding
    message.set_content(self.html_body, subtype='html', cte='quoted-printable')
    return message

  def __bytes__(self):
    return bytes(self.email_message)
