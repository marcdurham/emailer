import email.headerregistry

from dataclasses import dataclass


@dataclass(frozen=True)
class Recipient():
  name: str = ''
  email: str = ''
  groups: tuple = ()
  highlights: tuple = ()

  @property
  def header(self):
    username, domain = self.email.split('@')
    return email.headerregistry.Address(self.name, username, domain)

  def add_highlight(self, highlight):
    return Recipient(
        self.name, self.email, self.groups, self.highlights + (highlight,))

  def add_group(self, group):
    return Recipient(
        self.name, self.email, self.groups + (group,), self.highlights)

  def is_active(self):
    return 'active' in self.groups

  def is_dryrun(self):
    return 'dryrun' in self.groups

  def is_test(self):
    return 'test' in self.groups
