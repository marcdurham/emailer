"""Fetch spreadsheet data."""


import gspread
import oauth2client.service_account as oauth


def fetch_values(*, key, auth):
  """Fetch all data from a Google Spreadsheet

  Args:
    key (str): Spreadsheet identifier.
    auth (dict): OAuth credentials

  Returns:
    dict: Sheet titles as keys and lists of lists of cells as values.

  Example:
    fetch_values(
        key='1PAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9I',
        auth=<See sample-config.yml under 'auth'>)
    {
      'Sheet1': [
        ['CellA1', 'CellB1', ...],
        ['CellA2', 'CellB2', ...],
        ...
      ],
      'Sheet2': ...
    }
  """
  scope = ['https://spreadsheets.google.com/feeds']
  creds = oauth.ServiceAccountCredentials.from_json_keyfile_dict(auth, scope)
  client = gspread.authorize(creds)
  spreadsheet = client.open_by_key(key)
  worksheets = spreadsheet.worksheets()
  return {ws.title: ws.get_all_values() for ws in worksheets}
