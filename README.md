Emailer
=============
[![Build Status](https://travis-ci.org/WhiteHalmos/emailer.svg?branch=master)](https://travis-ci.org/WhiteHalmos/emailer)

Data Format
-----------------------
- `Emails`
  - First column is names (see special names in `emailer/name.py`)
  - Second column is default values for each name
  - Next column(s) is one email each, with values replaced by default if empty
- `Recipients`
  - Each row is one recipient made up of:
    - Email
    - Groups they are members of (e.g. Active, Dryrun)
    - Any number of highlights (this can be a name in the `Emails` sheet)

Usage
-----
    usage: email [-h] [-c CONFIG_DIR] [-k [KEY_NAMES [KEY_NAMES ...]]]
                 [--all-keys] [-d DATE] [-v] [-V] [--sample-config] [--active]
                 [--dryrun] [--test]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_DIR, --config-dir CONFIG_DIR
                            Directory containing config file. Default is current
                            working directory.
      -k [KEY_NAMES [KEY_NAMES ...]], --key-names [KEY_NAMES [KEY_NAMES ...]]
                            Key name(s) matching key(s) in the config.
      --all-keys            Run for all available keys in config.
      -d DATE, --date DATE  Date for which to send emails (YYYY-MM-DD). The
                            default is today.
      -v, --verbose         Display more logging output
      -V, --version         Print the current emailer module version.
      --sample-config       Print a sample config. Save as emailer.json or
                            .emailer.json.
      --active              Send emails to all active recipients.
      --dryrun              Send emails one day early to dryrun recipients.
      --test                Send emails only to test recipients.
* Enable the [Gmail](https://developers.google.com/gmail/api/quickstart/python)
  and [Sheets](https://developers.google.com/sheets/api/quickstart/python) APIs.
* Set up a config json file using `--sample-config`
    * Save the result as `emailer.json` in home dir.
    * The spreadsheet key is the long entry in the URL:
      `https://docs.google.com/spreadsheets/<key>/edit`
