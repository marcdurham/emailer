import logging

from . import api, auth, composer, config, fetcher, parser
from .gmailsender import GmailSender
from .messagebuilder import create_message_for_recipient
from .send import send_messages
from .name import SUBJECT, BODY, EMAILS, RECIPIENTS, PREFIX


def get_messages(data, date, group, extra_recipients, extra_values):
  emails = parser.parse_emails_for_date(data.get(EMAILS), date)
  recipients = parser.parse_recipients_in_group(data.get(RECIPIENTS), group)
  all_recipients = [*recipients, *extra_recipients]
  prefix = composer.get_prefix_for_group(group)
  for email in emails:
    values = composer.replace_values({PREFIX: prefix, **email, **extra_values})
    subject = prefix + composer.substitute_for_key(SUBJECT, values)
    body = composer.substitute_for_key(BODY, values)
    logging.info(body)
    for recipient in all_recipients:
      if recipient.is_valid():
        yield create_message_for_recipient(recipient, subject, body, values)


def get_config(config_dir):
  config_path = config.find_config_file(config_dir)
  config_obj = config.load_from_file(config_path)
  config_obj.validate()
  # Accessing creds either creates new creds or uses serialized creds.
  creds = config_obj.creds
  config_obj = config_obj.set_serialized_creds(auth.serialize(creds))
  config_obj.save_to_file(config_path)
  return config_obj


def process_sheets(group, config_dir, key_names, all_keys, date, skip): # pylint: disable=too-many-arguments
  config_obj = get_config(config_dir)
  if all_keys:
    sheet_ids = config_obj.get_all_keys()
  else:
    sheet_ids = config_obj.get_keys(key_names)
  for sheet_id in sheet_ids:
    data = fetcher.values(sheet_id, api.sheets(config_obj.creds))
    extra_recipients = config_obj.get_extra_recipients_for_group(group)
    extra_values = config_obj.get_extra_values()
    messages = get_messages(data, date, group, extra_recipients, extra_values)
    sender = GmailSender(api.gmail(config_obj.creds))
    send_messages(messages, sender, skip)
