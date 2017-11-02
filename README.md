Emailer
=============

    usage: email [-h] [-n] [-t] [-a] [-k KEY [KEY ...]] [--config CONFIG]
                 [--date DATE] [-v]

    Send emails

    optional arguments:
      -h, --help            show this help message and exit
      -n, --dryrun
      -t, --test
      -a, --all
      -k KEY [KEY ...], --key KEY [KEY ...]
                            Default is all keys
      --config CONFIG       The config.yml file, default at ~/.emailer/config.yml
      --date DATE           Run as if this was today
      -v, --verbose

* Create local config in `./config.yml` from `./config.yml.example`.
    * The key is the long entry in the URL: `https://docs.google.com/spreadsheets/<key>/edit`
* Set up the auth key according to [gspread's guide](http://gspread.readthedocs.org/en/latest/oauth2.html).
* The most used command is likely `./main.py -t`, this sends a test email to the sender.
* Follow [Google's python style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html).

