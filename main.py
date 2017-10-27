#!/usr/bin/env python3
'''
Desperately needs a new meaning in life other than 'everything'.
'''

import argparse
import datetime
import re
import sys

import premailer
import yaml

import data
import models
import utils

from pprint import pprint


DATE_FORMAT = '%B %d, %Y'
TIME_FORMAT = '%I:%M %p'
KEYMAP_FILE = 'keymap.yml'
REPLY_TO_KEY = 'reply-to'
SPEAKER_KEY = 'speaker'
HIGHLIGHT = '<strong style="background-color: yellow">{}</strong>'
VERBOSE = False


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
        pprint(len(messages))
    send(messages)


def get_datedata(loader, template_date, dryrun, test):
    today = template_date or datetime.date.today()
    one_day = datetime.timedelta(days=1)
    if dryrun:
        return loader.fetch_date(today + one_day)
    datedata = loader.fetch_date(today)
    if test and not datedata:
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


def run_template(loader, sender, server, datedata, dryrun, test, to):
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
    if to:
        group = []
        for recipient in to:
            if recipient in people:
                group.append(people[recipient])
            else:
                print('Cannot find {} in people {}.'.format(
                    recipient, to))
    elif test:
        if 'test' in groups:
            group = groups['test']
        else:
            from local import ME
            group = [ME]
        context['prefix'] = 'TEST - '
        official = False
    elif dryrun:
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


def run(args):
    global VERBOSE
    VERBOSE = VERBOSE or args.verbose

    template_date = None
    if args.date:
        template_date = utils.parse_date(args.date)

    if args.gmail:
        from local import GMAIL
        server = models.Gmail(
                user=GMAIL['sender'].email, password=GMAIL['password'])
        sender = GMAIL['sender']
    else:
        from local import MAILGUN
        server = models.MailGun(
                host=MAILGUN['host'], api_key=MAILGUN['api_key'])
        sender = MAILGUN['sender']

    loaders = []
    if args.directory:
        for directory in args.directory:
            loaders.append(data.YAMLLoader(directory=directory))
    else:
        with open(KEYMAP_FILE, 'r') as keymap_file:
            keymap = yaml.load(keymap_file)
            indexes = args.key or args.name
            for index in indexes:
                assert index in keymap, 'Key or Name not found in keymap file.'
                value = keymap[index]
                if args.key:
                    loaders.append(data.GSpreadLoader(key=value))
                elif args.name:
                    loaders.append(data.GSpreadLoader(name=value))

    for loader in loaders:
        datedata = get_datedata(loader, template_date, args.dryrun, args.test)
        run_template(loader, sender, server, datedata, args.dryrun, args.test,
                     args.to)


def main():
    parser = argparse.ArgumentParser(description='Send emails')
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-n', '--dryrun', action='store_true')
    action_group.add_argument('-t', '--test', action='store_true')
    action_group.add_argument('-c', '--cron', action='store_true')
    data_group = parser.add_mutually_exclusive_group(required=True)
    data_group.add_argument('-d', '--directory', nargs='+')
    data_group.add_argument('-k', '--key', nargs='+')
    data_group.add_argument('-m', '--name', nargs='+')
    parser.add_argument('--to', nargs='*')
    parser.add_argument('--date')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--gmail', action='store_true')
    run(parser.parse_args())


if __name__ == '__main__':
    main()

