import logging
import sys

from . import (api, args, auth, composer, config, fetcher, markdown, parser,
               sender)
from .message import Message
from .name import SUBJECT, BODY, FROM, REPLY_TO


def get_message_for_recipient(recipient, subject, markdown_body, values):
  body = markdown.mark_text(markdown_body, recipient.highlights, values)
  sender = composer.get_recipient(FROM, values)
  replyto = composer.get_recipient(REPLY_TO, values)
  return Message(subject=subject, sender=sender, recipient=recipient,
                 replyto=replyto, body=body)


def get_messages(data, date, group, extra_recipients, extra_values):
  emails = parser.parse_emails_for_date(data['Emails'], date)
  recipients = parser.parse_recipients_in_group(data['Recipients'], group)
  all_recipients = [*recipients, *extra_recipients]
  subject_prefix = composer.get_prefix_for_group(group)
  for email in emails:
    values = composer.replace_values({**email, **extra_values})
    subject = subject_prefix + composer.substitute_for_key(SUBJECT, values)
    text_body = composer.substitute_for_key(BODY, values)
    markdown_body = markdown.convert(text_body)
    for recipient in all_recipients:
      yield get_message_for_recipient(recipient, subject, markdown_body, values)


def main():
  options = args.get_options()
  logging.basicConfig(level=args.get_log_level(options))
  sys.stdout.write(args.get_version(options))
  sys.stdout.write(args.get_sample_config(options))
  config_path = config.find_config_file(options.config_dir)
  config_obj = config.load_from_file(config_path)
  config_obj.validate()
  creds = auth.creds(config_obj.serialized_creds, config_obj.client_secret)
  config_obj = config_obj.set_serialized_creds(auth.serialize(creds))
  config_obj.save_to_file(config_path)
  sheet_ids = config_obj.get_keys(options.key_names)
  groups = args.get_groups(options)
  for sheet_id in sheet_ids:
    data = fetcher.values(sheet_id, api.sheets(creds))
    for group in groups:
      date = args.get_date(options, group)
      extra_recipients = config_obj.get_extra_recipients_for_group(group)
      extra_values = config_obj.get_extra_values()
      messages = get_messages(data, date, group, extra_recipients, extra_values)
      sender.send_messages(messages, api.gmail(creds))


if __name__ == '__main__':
  main()
