Emailer
=============
[![Build Status](https://travis-ci.org/WhiteHalmos/emailer.svg?branch=master)](https://travis-ci.org/WhiteHalmos/emailer)

Data format
-----------------------
- `Emails`: Each row is one email with default values and overridden values
- `Recipients`: Each row is one recipient
- `General`: General information that do not change per email
- `Shortcuts`: Abbreviations for values
- `Templates`: Lengthy values that do not change per email

Ideas
-----
- ..

Usage
-----
    usage: email [-h] [-n] [-t] [-a] [-k KEY [KEY ...]] [--config CONFIG]
                 [--date DATE] [-v] [-s] [--sample-config] [--version]

    Send emails

    optional arguments:
      -h, --help            show this help message and exit
      -n, --next-day
      -t, --test
      -a, --all
      -k KEY [KEY ...], --key KEY [KEY ...]
                            Default is all keys
      --config CONFIG       The config file, default at ~/.emailer/config.yml
      --date DATE           Run as if this was today
      -v, --verbose
      -s, --skip-send       Test everything except actually sending emails
      --sample-config       Print a sample config.yml file to stdout
      --version             Print package version
* Enable the [Gmail](https://developers.google.com/gmail/api/quickstart/python)
  and [Sheets](https://developers.google.com/sheets/api/quickstart/python) APIs.
* Create local config with `email --sample-config >> ~/.emailer/config.yml`
    * The key is the long entry in the URL: `https://docs.google.com/spreadsheets/<key>/edit`
* The most used command is likely `email -t`, this sends a test email to the sender

