import logging
from . import api, args, auth, composer, config, fetcher, parser, sender


def get_messages(data, date, group):
  recipients = parser.parse_recipients_in_group(data['Recipients'], group)
  general = parser.parse_general(data['General'])
  shortcuts = parser.parse_general(data['Shortcuts'])
  markdown = parser.parse_general(data['Markdown'])
  for email in parser.parse_emails_for_date(data['Emails'], date):
    body = composer.compose_body(email, shortcuts, markdown)
    for recipient in recipients:
      yield composer.compose_for_recipient(recipient, body)


def main():
  options = args.get_options()
  logging.basicConfig(level=args.get_log_level(options))
  config_path = config.find_config_file(options.config_dir)
  config_obj = config.load_from_file(config_path)
  creds = auth.creds(config_obj.serialized_creds, config_obj.client_secret)
  config_obj = config_obj.set_serialized_creds(auth.serialize(creds))
  config_obj.save_to_file(config_path)
  gmail = api.gmail(creds)
  sheets = api.sheets(creds)
  keys = config_obj.get_keys(options.key_names)
  groups = args.get_groups(options)
  for key in keys:
    data = fetcher.values(key, sheets)
    for group in groups:
      date = args.get_date(options.date, group)
      messages = get_messages(data, date, group)
      sender.send_messages(messages, gmail)


if __name__ == '__main__':
  main()
