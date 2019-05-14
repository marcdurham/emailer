import dataclasses

from .emailvalidator import is_email_valid


@dataclasses.dataclass(frozen=True)
class Recipient():
  email: str = ''
  groups: tuple = ()
  highlights: tuple = ()

  def is_valid(self):
    return is_email_valid(self.email)
