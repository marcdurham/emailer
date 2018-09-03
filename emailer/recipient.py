import dataclasses  # pylint: disable=wrong-import-order
import email.headerregistry


@dataclasses.dataclass(frozen=True)
class Recipient():
  email: str = ''
  groups: tuple = ()
  highlights: tuple = ()

  @property
  def header(self):
    return email.headerregistry.Address(addr_spec=self.email)

  def in_group(self, group):
    return group in self.groups
