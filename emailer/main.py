'''
Desperately needs a new meaning in life other than 'everything'.
'''

import argparse
import datetime
import os
import re
import sys

import premailer
import yaml

from . import data, models, utils

from pprint import pprint


DATE_FORMAT = '%B %d, %Y'
TIME_FORMAT = '%I:%M %p'
KEYMAP_FILE = 'keymap.yml'
REPLY_TO_KEY = 'reply-to'
SPEAKER_KEY = 'speaker'
HIGHLIGHT = '<strong style="background-color: yellow">{}</strong>'
VERBOSE = False
ALL = 'all'
DRYRUN = 'dryrun'
TEST = 'test'


class LiteralDefault(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def format_value(value, people):
    if value is None:
        ret = ''
    elif isinstance(value, int):
        ret = str(value)
    elif isinstance(value, datetime.date):
        ret = datetime.date.strftime(value, DATE_FORMAT)
    elif re.match(r'\d{2}/\d{2}/\d{4}', value):
        ret = datetime.date.strftime(utils.parse_date(value), DATE_FORMAT)
    elif re.match(r'\d{2}:\d{2}:\d{2}', value):
        digits = map(int, value.split(':'))
        ctime = datetime.time(*digits)
        ret = datetime.time.strftime(ctime, TIME_FORMAT)
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
            template = template.replace(h, HIGHLIGHT.format(h))

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
    if SPEAKER_KEY in context and official:
        speaker = context['speaker']
        if speaker in people:
            group.append(people[speaker])
    sent_already = set()
    for person in group:
        if not person.has_valid_email():
            continue
        if person.email in sent_already:
            if VERBOSE:
                print('Already sent to ' + str(person))
            continue
        sent_already.add(person.email)
        if VERBOSE:
            print('Formatting email for {}.'.format(str(person)))
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
    if VERBOSE:
        print('Sending all emails.')
        print(len(messages))
        if messages:
            pprint(messages[0].html)
    send(messages)


def get_datedata(loader, today, email_type):
    one_day = datetime.timedelta(days=1)
    if email_type == DRYRUN:
        return loader.fetch_date(today + one_day)
    datedata = loader.fetch_date(today)
    if email_type == TEST and not datedata:
        new_day = today
        for i in range(10):
            new_day -= one_day
            datedata = loader.fetch_date(new_day)
            if datedata:
                return datedata
        new_day = today
        for i in range(10):
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
    default_context = loader.fetch_default_context()
    if VERBOSE:
        print('Sending email for {}.'.format(
                datedata[data.DATE].strftime(DATE_FORMAT)))
    context = default_context.copy()
    utils.update_if_not_none(context, datedata[data.CONTEXT])
    section_list = datedata[data.SECTIONS]
    group = groups[context['group']]
    official = True
    highlight = True
    if email_type == TEST:
        if 'test' in groups:
            group = groups['test']
        else:
            group = [sender]
        context['prefix'] = 'TEST - '
        official = False
    elif email_type == DRYRUN:
        group = groups['dryrun']
        context['prefix'] = 'DRYRUN - '
        official = False
        highlight = False
    if REPLY_TO_KEY in context:
        reply_to = people[context[REPLY_TO_KEY]]
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


def run(types, today, config):
    server = models.MailGun(host=config['mailgun']['host'],
                            api_key=config['mailgun']['api_key'])
    sender = models.Person(name=config['sender']['name'],
                           email=config['sender']['email'])
    keys = config['keys'].keys()
    loaders = [data.GSpreadLoader(key=config['keys'][key], auth=config['auth'])
               for key in keys]
    for loader in loaders:
        for email_type, should_run in types.items():
            if not should_run:
                continue
            datedata = get_datedata(loader, today, email_type)
            run_template(loader, sender, server, datedata, email_type)


def get_parser():
    parser = argparse.ArgumentParser(description='Send emails')
    parser.add_argument('-n', '--dryrun', action='store_true')
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-a', '--all', action='store_true')
    parser.add_argument('-k', '--key', nargs='+')
    parser.add_argument('--config', help='config.yml file')
    parser.add_argument('--date', help='Run as if this was today')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser


def main():
    global VERBOSE
    options = get_parser().parse_args()
    assert options.all or options.dryrun or options.test, (
            'At least one action is needed')
    VERBOSE = VERBOSE or options.verbose
    types = {}
    types[ALL] = options.all
    types[DRYRUN] = options.dryrun
    types[TEST] = options.test
    if options.date:
        today = utils.parse_date(args.date)
    else:
        today = datetime.date.today()
    if not options.config:
        options.config = os.path.expanduser('~/.emailer/config.yml')
    with open(options.config, 'r') as config_file:
        config = yaml.load(config_file)
    if options.key:
        config['keys'] = {k: config['keys'][k] for k in options.key}
    run(types, today, config)
