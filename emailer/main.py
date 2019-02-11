from . import args, shell

def main():
  options = args.get_options()
  if options.version:
    print(args.get_version())
  elif options.sample_config:
    print(args.get_sample_config())
  else:
    shell.set_log_level(args.get_log_level(options))
    shell.process_sheets(options)


if __name__ == '__main__':
  main()
