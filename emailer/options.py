import datetime
import logging


class Options():

  def __init__(self, options):
    self.options = options

  @property
  def log_level(self):
    if self.verbose:
      return logging.INFO
    return logging.WARNING

  @property
  def group(self):
    if self.active:
      return 'active'
    if self.dryrun:
      return 'dryrun'
    if self.test:
      return 'test'
    return None

  @property
  def send_date(self):
    if self.group == 'dryrun':
      date = datetime.date.fromisoformat(self.date)
      return (date + datetime.timedelta(days=1)).isoformat()
    return self.date

  def __getattr__(self, name):
    '''Pass through implicit attributes.'''
    if hasattr(self.options, name):
      return getattr(self.options, name)
    return None
