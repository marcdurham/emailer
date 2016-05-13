Auto Emailer
=============

Installation
--------------
* Create local config in `./local.py`.
    * The three attributes required in this file are specified in `./local.py.example`.
* Copy local keymap shortcut from `./keymap.yml.example` to `./keymap.yml`.
    * You can set up keymap.yml's entries to be the actual id of the Google spreadsheet file, or the file name.
    * The id is the long entry in the URL: `https://docs.google.com/spreadsheets/d<key>/edit`
    * The name can simply be the exact name of the spreadsheet.
    * This depends on the argument you pass into `./main.py`.
* Set crontab entries.
    * Crontab examples for setting up recurring automatic sends are located in `./crontab.example`.
    * Currently I use python from a virtualenv, thus the `.virtualenv` path invocation of the python binary.
* Install python requirements (recommended in virtualenv).
    * `pip install -r requirements.txt`
* Set up private.json according to [gspread's guide](http://gspread.readthedocs.org/en/latest/oauth2.html).

Usage
----------
```
usage: main.py [-h] (-n | -t | -c) [-d DIRECTORY | -k KEY | -m NAME]
               [--to [TO [TO ...]]] [--date DATE] [-v]

Send emails

optional arguments:
  -h, --help            show this help message and exit
  -n, --dryrun
  -t, --test
  -c, --cron
  -d DIRECTORY, --directory DIRECTORY
  -k KEY, --key KEY
  -m NAME, --name NAME
  --to [TO [TO ...]]
  --date DATE
  -v, --verbose
```
* The most used command is likely `./main.py -t -m example-group`, this sends a test email to `local.ME`.

Style
----------
* I follow [Google's python style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html).

