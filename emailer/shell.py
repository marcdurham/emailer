import os
from . import api, args, config


def get_creds(config_dir):
  config_path = config.find_config_file(config_dir)
  config_obj = config.load_from_file(config_path)
  creds = auth.creds(config_obj.serialized_creds, config_obj.client_secret)
  config_obj = config.set_serialized_creds(auth.serialize(creds))
  config_obj.save_to_file(config_path)
  return creds


def main():
  options = args.get_options()
  creds = get_creds(options.config_dir)
  gmail = api.gmail(creds)
  sheets = api.sheets(creds)


if __name__ == '__main__':
  main()
