import email.message

import attr


@attr.s(frozen=True)
class Message():
  subject = attr.ib(default='')
  sender = attr.ib(default=None)
  recipient = attr.ib(default=None)
  replyto = attr.ib(default=None)
  body = attr.ib(default='')

  @property
  def email_message(self):
    message = email.message.EmailMessage()
    message['Subject'] = self.subject
    if self.sender:
      message['From'] = self.sender.header
    if self.recipient:
      message['To'] = self.recipient.header
    if self.replyto:
      message['Reply-To'] = self.replyto.header
    # TODO: Figure out what cte is and whether it is necessary
    message.set_content(self.body, subtype='html', cte='quoted-printable')
    return message
