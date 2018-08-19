import email.headerregistry

import attr


@attr.s(frozen=True)
class Recipient():
  name = attr.ib(default='')
  email = attr.ib(default='')
  groups = attr.ib(factory=tuple)
  highlights = attr.ib(factory=tuple)

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
