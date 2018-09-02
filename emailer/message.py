import base64
import dataclasses  # pylint: disable=wrong-import-order
import email.message

from .recipient import Recipient


@dataclasses.dataclass(frozen=True)
class Message():
  subject: str = ''
  sender: Recipient = None
  receiver: Recipient = None
  replyto: Recipient = None
  body: str = ''

  @property
  def email_message(self):
    message = email.message.EmailMessage()
    message['Subject'] = self.subject
    if self.sender:
      message['From'] = self.sender.header
    if self.receiver:
      message['To'] = self.receiver.header
    if self.replyto:
      message['Reply-To'] = self.replyto.header
    # TODO: Figure out what cte is and whether it is necessary
    message.set_content(self.body, subtype='html', cte='quoted-printable')
    return message

  @property
  def gmail_body(self):
    return {'raw': base64.urlsafe_b64encode(self.as_bytes()).decode()}

  def as_bytes(self):
    return self.email_message.as_bytes()
