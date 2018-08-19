import gspread
import oauth2client.service_account as oauth


def fetch_values(*, key, auth):
  '''Fetch all data from a Google Spreadsheet

  Returns a dict with titles as keys and cells in lists of lists as values.
  '''
  scope = ['https://spreadsheets.google.com/feeds']
  creds = oauth.ServiceAccountCredentials.from_json_keyfile_dict(auth, scope)
  client = gspread.authorize(creds)
  spreadsheet = client.open_by_key(key)
  worksheets = spreadsheet.worksheets()
  return {ws.title: ws.get_all_values() for ws in worksheets}
