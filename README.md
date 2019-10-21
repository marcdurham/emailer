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
                 [--all-keys] [-d DATE] [-v] [-V] [--sample-config] [--skip-send]
                 [--save-sheet-to SAVE_SHEET_TO] [--stdin] [--stdout-markdown]
                 [--stdout-email] [--active | --dryrun | --test]
    
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
      -V, --version         Print the current emailer module version and exit.
      --sample-config       Print a sample config. Save as emailer.json or
                            .emailer.json and exit.
      --skip-send           Avoid actually sending emails, useful for testing.
      --save-sheet-to SAVE_SHEET_TO
                            Save the sheet into the following JSON file.
      --stdin               Use STDIN to get the sheet data, instead of directly
                            from Google Sheets.
      --stdout-markdown     Print a JSON array of unhighlighted email,still in
                            markdown.
      --stdout-email        Print a JSON array all highlighted email messages.
      --active              Send emails to all active recipients.
      --dryrun              Send emails one day early to dryrun recipients.
      --test                Send emails only to test recipients.
      
### Examples

Send a message for today's date to all Active recipients on the list `mykey`:
```bash
python -m emailer -k mykey --active
```

See what would happen if today's email went out, but don't actually send email:
```bash
python -m emailer -k mkey --active --verbose --skip-send
```

Send a dryrun version of tomorrow's email to DryRun recipients:
```bash
python -m emailer -k mykey --dryrun
```

Send a dryrun version of a specific date to the DryRun recipients.
```bash
python -m emailer -k mykey --dryrun -d 2019-10-20
```

Provide a cached json sheet, and return a list of email (doesn't send or lookup anything on the server):
```bash
cat sheet.json | python -m emailer -k mkey --active --skip-send --stdin --stdout-email
[
    "Subject: Schedule for 2019-10-26\nFrom: Schedule Emailer <me@example.com>\nTo: alice@example.com\nReply-To: Robert Wallis <robert@example.com>\nContent-Type: text/html; charset=\"utf-8\"\nContent-Transfer-Encoding: quoted-printable\nMIME-Version: 1.0\n\n<p>=No Meeting Today</p>\n",
    "Subject: Schedule for 2019-10-26\nFrom: Schedule Emailer <me@example.com>\nTo: bob@example.com\nReply-To: Robert Wallis <robert@example.com>\nContent-Type: text/html; charset=\"utf-8\"\nContent-Transfer-Encoding: quoted-printable\nMIME-Version: 1.0\n\n<p>=No Meeting Today</p>\n",
]    
```

Get the sheet from Google Sheets and cache it.
```bash
python -m emailer -k mykey --test --skip-send --save-sheet-to sheet.json
```

Setup
-----
* Enable the [Gmail](https://developers.google.com/gmail/api/quickstart/python)
  and [Sheets](https://developers.google.com/sheets/api/quickstart/python) APIs.
  * Download `credentials.json` to be used in the config file.
* Set up a config json file using `--sample-config`
  * Save the result as `emailer.json` in home dir.
  * The spreadsheet key is the long entry in the URL:
    `https://docs.google.com/spreadsheets/<key>/edit`
* In case of Google API errors, check the
  [GSuite Dashboard](https://www.google.com/appsstatus#hl=en&v=status).

Development
-----------
* `pipenv` can be installed using [pipx](https://github.com/cs01/pipx).
    * For packaging, `tox` and `twine` are also necessary.
* Use `make init` to initialize the dev virtual environment.
* Use `make` to run all tests, including lint and coverage.
* If necessary, use `pipenv update` to update `Pipfile.lock`.
