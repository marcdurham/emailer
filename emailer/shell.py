import logging
import time

from . import api, auth, composer, config, fetcher, markdown, parser
from .gmailsender import GmailSender
from .send import send_message
from .message import Message
from .name import SUBJECT, BODY, FROM, REPLY_TO, EMAILS, RECIPIENTS


def get_message_for_recipient(recipient, subject, body, values):
  highlighted_body = markdown.mark_text(body, recipient.highlights, values)
  html_body = markdown.convert(highlighted_body)
  sender = composer.get_recipient(FROM, values)
  replyto = composer.get_recipient(REPLY_TO, values)
  return Message(subject=subject, sender=sender, recipient=recipient,
                 replyto=replyto, html_body=html_body)


def get_messages(data, date, group, extra_recipients, extra_values):
  emails = parser.parse_emails_for_date(data.get(EMAILS), date)
  recipients = parser.parse_recipients_in_group(data.get(RECIPIENTS), group)
  all_recipients = [*recipients, *extra_recipients]
  subject_prefix = composer.get_prefix_for_group(group)
  for email in emails:
    values = composer.replace_values({**email, **extra_values})
    subject = subject_prefix + composer.substitute_for_key(SUBJECT, values)
    body = composer.substitute_for_key(BODY, values)
    logging.info(body)
    for recipient in all_recipients:
      yield get_message_for_recipient(recipient, subject, body, values)


def get_config_and_creds(config_dir):
  config_path = config.find_config_file(config_dir)
  config_obj = config.load_from_file(config_path)
  config_obj.validate()
  creds = auth.creds(config_obj.serialized_creds, config_obj.client_secret)
  config_obj = config_obj.set_serialized_creds(auth.serialize(creds))
  config_obj.save_to_file(config_path)
  return config_obj, creds


def process_sheets(group, config_dir, key_names, all_keys, date, skip): # pylint: disable=too-many-arguments,too-many-locals
  config_obj, creds = get_config_and_creds(config_dir)
  sheet_ids = config_obj.get_keys(key_names, all_keys)
  for sheet_id in sheet_ids:
    data = fetcher.values(sheet_id, api.sheets(creds))
    extra_recipients = config_obj.get_extra_recipients_for_group(group)
    extra_values = config_obj.get_extra_values()
    messages = get_messages(data, date, group, extra_recipients, extra_values)
    sender = GmailSender(api.gmail(creds))
    for message in messages:
      send_message(message=message, sender=sender, skip=skip)
      time.sleep(1) # Avoids 500: Backend Error.
