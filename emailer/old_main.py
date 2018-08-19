import argparse
import datetime
import os
import re

import premailer
import yaml

from . import data, models, utils, __version__ as emailer_version
from .fetcher import fetch_values


_DATE_FORMAT = '%B %d, %Y'
_TIME_FORMAT = '%I:%M %p'
_REPLY_TO_KEY = 'reply-to'
_SPEAKER_KEY = 'speaker'
_HIGHLIGHT = '<strong style="background-color: yellow">{}</strong>'
_ALL = 'all'
_DRYRUN = 'dryrun'
_TEST = 'test'
_SOURCE_DIR = os.path.dirname(__file__)
_SAMPLE_CONFIG_FILE = os.path.join(_SOURCE_DIR, 'sample-config.yml')


class LiteralDefault(dict):
  def __missing__(self, key):
    return '{' + key + '}'


def format_value(value, people):
  if value is None:
    ret = ''
  elif isinstance(value, int):
    ret = str(value)
  elif isinstance(value, datetime.date):
    ret = datetime.date.strftime(value, _DATE_FORMAT)
  elif re.match(r'\d{2}/\d{2}/\d{4}', value):
    digits = map(int, value.split(':'))
    ctime = datetime.time(*digits)
    ret = datetime.time.strftime(ctime, _TIME_FORMAT)
  elif value in people:
    ret = people[value].name
  else:
    ret = value
  return ret


def format_template(template, templates, context, people, highlights=None):
  values = LiteralDefault(templates)
  values.update({abbrev: person.name for abbrev, person in people.items()})
  values.update({
      name: format_value(value, people)
      for name, value in context.items()
  })
  literals = {}
  for key, value in values.items():
    if key.endswith('-literal'):
      literals[key] = value
      values[key] = '{' + key + '}'
  # Format many times when template is used in value.
  while True:
    new_value = template.format_map(values)
    if new_value == template:
      break
    template = new_value

  if highlights:
    for h in highlights:
      template = template.replace(h, _HIGHLIGHT.format(h))

  if literals:
    for key, value in literals.items():
      values[key] = value
    template = template.format_map(values)
  return template


def generate_body(templates, sections, context, people, highlights=None):
  return '\n'.join([
      format_template(templates.get(name, name), templates, context, people,
                      highlights)
      for name in sections])


def format_and_send(send, sender, group, templates, sections, context, people,
                    reply_to=None, official=None, highlight=None):
  assert 'subject' in templates, 'Missing "subject" template.'
  subject = format_template(templates['subject'], templates, context, people)
  messages = []
  # Special case for sending email to visiting speakers
  if _SPEAKER_KEY in context and official:
    speaker = context[_SPEAKER_KEY]
    for person in people.values():
      # Allow extraneous characters in name and multiple speakers, but require
      # that the person's full name be listed
      if person.name in speaker:
        group.append(person)
  sent_already = set()
  for person in group:
    if not person.has_valid_email():
      continue
    if person.email in sent_already:
      continue
    sent_already.add(person.email)
    if highlight:
      highlights = [format_value(h, people) for h in person.highlights]
    else:
      highlights = None
    body = generate_body(
        templates, sections, context, people, highlights)
    body = premailer.transform(body)
    message = models.Message()
    message.sender = sender
    message.recipient = person
    message.subject = subject
    message.html = body
    if reply_to:
      message.reply_to = reply_to
    messages.append(message)
  send(messages)


def get_datedata(loader, today, email_type):
  one_day = datetime.timedelta(days=1)
  if email_type == _DRYRUN:
    return loader.fetch_date(today + one_day)
  datedata = loader.fetch_date(today)
  if email_type == _TEST and not datedata:
    new_day = today
    for _ in range(10):
      new_day -= one_day
      datedata = loader.fetch_date(new_day)
      if datedata:
        return datedata
    new_day = today
    for _ in range(10):
      new_day += one_day
      datedata = loader.fetch_date(new_day)
      if datedata:
        return datedata
  return datedata


def run_template(loader, sender, server, datedata, email_type):
  if not datedata:
    return
  people = loader.fetch_people()
  groups = loader.fetch_groups()
  templates = loader.fetch_templates()
  context = datedata[data.CONTEXT]
  section_list = datedata[data.SECTIONS]
  group = groups[context['group']]
  official = True
  highlight = True
  if email_type == _TEST:
    if 'test' in groups:
      group = groups['test']
    else:
      group = [sender]
    context['prefix'] = 'TEST - '
    official = False
  elif email_type == _DRYRUN:
    group = groups['dryrun']
    context['prefix'] = 'DRYRUN - '
    official = False
    highlight = False
  if _REPLY_TO_KEY in context:
    reply_to = people[context[_REPLY_TO_KEY]]
  else:
    reply_to = None
  format_and_send(
      send=server.send,
      sender=sender,
      group=group,
      templates=templates,
      sections=section_list,
      context=context,
      people=people,
      reply_to=reply_to,
      official=official,
      highlight=highlight)


def run(types, today, config, skip_send):
  if 'mailgun' in config:
    server = models.MailGun(host=config['mailgun']['host'],
                            api_key=config['mailgun']['api_key'],
                            skip_send=skip_send)
  elif 'gmail' in config:
    server = models.Server(user=config['gmail']['user'],
                           password=config['gmail']['password'],
                           skip_send=skip_send)
  else:
    raise Exception('No valid authentication protocol in config file')
  sender = models.Person(name=config['sender']['name'],
                         email=config['sender']['email'])
  keys = config['keys'].keys()
  options = config.get('options', dict())
  from pprint import pprint
  for key in keys:
    pprint(fetch_values(key=config['keys'][key], auth=config['auth'])['Context'])
  #loaders = [data.GSpreadLoader(key=config['keys'][key], auth=config['auth'],
  #                              newline_to_br=options.get('newline-to-br'))
  #           for key in keys]
  #for loader in loaders:
  #  for email_type, should_run in types.items():
  #    if not should_run:
  #      continue
  #    datedata = get_datedata(loader, today, email_type)
  #    run_template(loader, sender, server, datedata, email_type)


def load_config(config=None):
  if not config:
    config = os.path.expanduser('~/.emailer/config.yml')
  with open(config, 'r') as config_file:
    return yaml.load(config_file)


def get_sample_config():
  with open(_SAMPLE_CONFIG_FILE, 'r') as f:
    return f.read()


def get_parser():
  parser = argparse.ArgumentParser(description='Send emails')
  parser.add_argument('-n', '--next-day', action='store_true')
  parser.add_argument('-t', '--test', action='store_true')
  parser.add_argument('-a', '--all', action='store_true')
  parser.add_argument('-k', '--key', nargs='+', help='Default is all keys')
  parser.add_argument('--config',
                      help='The config file, default at ~/.emailer/config.yml')
  parser.add_argument('--date', help='Run as if this was today')
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('-s', '--skip-send', action='store_true',
                      help='Test everything except actually sending emails. '
                           'Also avoids sending delay.')
  parser.add_argument('--sample-config', action='store_true',
                      help='Print a sample config.yml file to stdout')
  parser.add_argument('--version', action='store_true',
                      help='Print package version')
  return parser


def main():
  options = get_parser().parse_args()
  if options.sample_config:
    print(get_sample_config())
  if options.version:
    print(emailer_version)
  types = {}
  types[_ALL] = options.all
  types[_DRYRUN] = options.next_day
  types[_TEST] = options.test
  if options.date:
    today = utils.parse_date(options.date)
  else:
    today = datetime.date.today()
  config = load_config(options.config)
  if options.key:
    config['keys'] = {k: config['keys'][k] for k in options.key}
  run(types, today, config, skip_send=options.skip_send)
