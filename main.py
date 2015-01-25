#!/usr/bin/env python3
'''
Desperately needs a new meaning in life other than 'everything'.
'''

import argparse
import datetime
import re
import sys

import yaml

import data
import models
import utils


DATE_FORMAT = '%B %d, %Y'
TIME_FORMAT = '%I:%M %p'
KEYMAP_FILE = 'keymap.yml'
REPLY_TO_KEY = 'reply-to'
VERBOSE = False


class Error(Exception):
    pass


def generate_body(templates, sections, context, people, highlight=None):
    return '\n'.join([
        format_template(templates[name], context, people, highlight)
        for name in sections])


def format_value(value, people, highlight=None):
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

    if highlight:
        return ret.replace(highlight, '<strong style="background-color: yellow">' + highlight + '</strong>')
    return ret


def format_template(template, context, people, highlight=None):
    return template.format_map({
        name: format_value(value, people, highlight)
        for name, value in context.items()})


def format_and_send(send, sender, group, templates, sections, context, people,
                    reply_to=None):
    assert 'subject' in templates, 'Missing "subject" template.'
    subject = format_template(templates['subject'], context, people)
    messages = []
    for person in group:
        if not person.has_valid_email():
            continue
        if VERBOSE:
            print('Formatting email for {}.'.format(str(person)))
        body = generate_body(templates, sections, context, people, person.name)
        message = models.Message()
        message.sender = sender
        message.recipient = person
        message.subject = subject
        message.html = body
        message.reply_to = reply_to
        messages.append(message)
    if VERBOSE:
        print('Sending all emails.')
    send(messages)


def run(args):
    global VERBOSE
    VERBOSE = VERBOSE or args.verbose

    template_date = None
    if args.date:
        template_date = utils.parse_date(args.date)

    from local import PASSWORD, SENDER, REPLY_TO, ME
    if VERBOSE:
        print('Logging into server as {}.'.format(str(SENDER)))
    server = models.Gmail(user=SENDER.email, password=PASSWORD)

    loader = None
    if args.directory:
        loader = data.YAMLLoader(directory=args.directory)
    elif args.key:
        with open(KEYMAP_FILE, 'r') as keymap_file:
            keymap = yaml.load(keymap_file)
            if args.key in keymap:
                args.key = keymap[args.key]
        loader = data.GSpreadLoader(
            username=SENDER.email, password=PASSWORD, key=args.key)
    assert loader is not None, 'Loader cannot be set up.'

    people = loader.fetch_people()
    groups = loader.fetch_groups()
    templates = loader.fetch_templates()
    default_context = loader.fetch_default_context()

    today = template_date or datetime.date.today()
    one_day = datetime.timedelta(days=1)
    if args.dryrun:
        today += one_day
    date_data = loader.fetch_date(today)
    if args.test and not date_data:
        for i in range(10):
            today -= one_day
            date_data = loader.fetch_date(today)
            if date_data:
                break
    if date_data:
        if VERBOSE:
            print('Sending email for {}.'.format(today.strftime(DATE_FORMAT)))
        context = default_context.copy()
        utils.update_if_not_none(context, date_data[data.CONTEXT])
        section_list = date_data[data.SECTIONS]
        group = groups[context['group']]
        if args.to:
            group = []
            for recipient in args.to:
                if recipient in people:
                    group.append(people[recipient])
                else:
                    print('Cannot find {} in people {}.'.format(
                        recipient, args.to))
        elif args.test:
            group = [ME]
            context['prefix'] = 'TEST - '
        elif args.dryrun:
            group = groups['dryrun']
            context['prefix'] = 'DRYRUN - '
        if REPLY_TO_KEY in context:
            reply_to = people[context[REPLY_TO_KEY]]
        else:
            reply_to = REPLY_TO
        format_and_send(
            send=server.send,
            sender=SENDER,
            group=group,
            templates=templates,
            sections=section_list,
            context=context,
            people=people,
            reply_to=reply_to)
    elif VERBOSE:
        print('No template found for {}.'.format(today.strftime(DATE_FORMAT)))


def main():
    parser = argparse.ArgumentParser(description='Send emails')
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-n', '--dryrun', action='store_true')
    action_group.add_argument('-t', '--test', action='store_true')
    action_group.add_argument('-c', '--cron', action='store_true')
    data_group = parser.add_mutually_exclusive_group()
    data_group.add_argument('-d', '--directory')
    data_group.add_argument('-k', '--key', default='kitchener')
    parser.add_argument('--to', nargs='*')
    parser.add_argument('--date')
    parser.add_argument('-v', '--verbose', action='store_true')
    run(parser.parse_args())


if __name__ == '__main__':
    main()

