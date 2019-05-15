import google.oauth2.credentials
import google_auth_oauthlib.flow as oauth_flow


def fetch_new_creds(config):
  return oauth_flow.InstalledAppFlow.from_client_config(config, scopes=[
      'https://www.googleapis.com/auth/gmail.send',
      'https://www.googleapis.com/auth/spreadsheets.readonly',
      ]).run_console()


def serialize(credentials):
  return {k: getattr(credentials, k) for k in (
      'token', 'refresh_token', 'token_uri', 'client_id', 'client_secret',
      'scopes')}


def create_or_deserialize_creds(serialized_creds, config=None):
  if serialized_creds:
    return google.oauth2.credentials.Credentials(**serialized_creds)
  return fetch_new_creds(config)
