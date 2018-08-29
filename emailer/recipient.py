import dataclasses
import email.headerregistry


@dataclasses.dataclass(frozen=True)
class Recipient():
  name: str = ''
  email: str = ''
  groups: tuple = ()
  highlights: tuple = ()

  @property
  def header(self):
    return email.headerregistry.Address(self.name, addr_spec=self.email)

  def add_highlight(self, highlight):
    return dataclasses.replace(self, highlights=self.highlights+(highlight,))

  def add_group(self, group):
    return dataclasses.replace(self, groups=self.groups+(group,))

  def is_active(self):
    return 'active' in self.groups

  def is_dryrun(self):
    return 'dryrun' in self.groups

  def is_test(self):
    return 'test' in self.groups
