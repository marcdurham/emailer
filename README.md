Emailer
=============

```
usage: email [-h] [-n] [-t] [-a] [-k KEY [KEY ...]] --config CONFIG --auth
             AUTH [--date DATE] [-v]

Send emails

optional arguments:
  -h, --help            show this help message and exit
  -n, --dryrun
  -t, --test
  -a, --all
  -k KEY [KEY ...], --key KEY [KEY ...]
  --config CONFIG       config.yml file
  --auth AUTH           private.json file
  --date DATE           Run as if this was today
  -v, --verbose
```
* Create local config in `./config.yml` from `./config.yml.example`.
    * The key is the long entry in the URL: `https://docs.google.com/spreadsheets/<key>/edit`
* Set up auth.json according to [gspread's guide](http://gspread.readthedocs.org/en/latest/oauth2.html).
* The most used command is likely `./main.py -t -k example-group`, this sends a test email to sender.

Style
----------
* I follow [Google's python style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html).

