Emailer
=============
[![Build Status](https://travis-ci.org/WhiteHalmos/emailer.svg?branch=master)](https://travis-ci.org/WhiteHalmos/emailer)

Data Format
-----------------------
- `Emails`: Each column is one email values overriding default
- `Recipients`: Each row is one recipient

Usage
-----
    usage: email [-h] [-c CONFIG_DIR] [-k KEY_NAMES] [-d DATE] [-v] [-V]
                 [--active] [--dryrun] [--test]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_DIR, --config-dir CONFIG_DIR
                            Directory containing config file. Default is current
                            working directory.
      -k KEY_NAMES, --key-name KEY_NAMES
                            Key name matching a key in the config. Default is all
                            available key names.
      -d DATE, --date DATE  Date for which to send emails (YYYY-MM-DD). The
                            default is today.
      -v, --verbose         Display more logging output
      -V, --version         Print the current emailer module version.
      --active              Send emails to all active recipients.
      --dryrun              Send emails one day early to dryrun recipients.
      --test                Send emails only to test recipients.
* Enable the [Gmail](https://developers.google.com/gmail/api/quickstart/python)
  and [Sheets](https://developers.google.com/sheets/api/quickstart/python) APIs.
* Set up a config json file using `--sample-config`
    * Save the result as `emailer.json` in home dir.
    * The spreadsheet key is the long entry in the URL:
      `https://docs.google.com/spreadsheets/<key>/edit`
