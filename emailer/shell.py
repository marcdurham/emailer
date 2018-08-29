import os
from . import api, args, auth, config, parser


def get_messages(data, date):
  emails = parser.parse_emails(data)
  recipients = parser.parse_recipients(data)
  return []


def main():
  options = args.get_options()
  config_path = config.find_config_file(options.config_dir)
  config_obj = config.load_from_file(config_path)
  creds = auth.creds(config_obj.serialized_creds, config_obj.client_secret)
  config_obj = config_obj.set_serialized_creds(auth.serialize(creds))
  config_obj.save_to_file(config_path)
  gmail = api.gmail(creds)
  sheets = api.sheets(creds)
  keys = config_obj.get_keys(option.key_names)
  for key in keys:
    data = fetcher.values(key, sheets)
    messages = get_messages(data, options.date)
    sender.send_messages(messages, gmail)


if __name__ == '__main__':
  main()
