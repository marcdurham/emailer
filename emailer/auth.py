import base64
import json
import os.path

import googleapiclient.discovery
import google.oauth2.credentials
import google_auth_oauthlib.flow


_SCOPES = [
    # https://developers.google.com/gmail/api/auth/scopes
    'https://www.googleapis.com/auth/gmail.send',
    # https://developers.google.com/sheets/api/guides/authorizing
    'https://www.googleapis.com/auth/spreadsheets.readonly',
]


def _fetch_new_tokens(creds_path):
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      creds_path, scopes=_SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
  auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
  print('Please go to this URL: {}'.format(auth_url))
  code = input('Enter the authorization code: ')
  flow.fetch_token(code=code)
  credentials = flow.credentials
  return {
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'token_uri': credentials.token_uri,
      'client_id': credentials.client_id,
      'client_secret': credentials.client_secret,
      'scopes': credentials.scopes,
  }


def _get_or_create_creds(config_dir):
  token_path = os.path.join(config_dir, 'token.json')
  if os.path.exists(token_path):
    with open(token_path, 'r') as token_file:
      tokens = json.load(token_file)
  else:
    creds_path = os.path.join(config_dir, 'client_secret.json')
    with open(token_path, 'w') as token_file:
      tokens = _fetch_new_tokens(creds_path)
      json.dump(tokens, token_file)
  return google.oauth2.credentials.Credentials(**tokens)


def authorize_gmail(config_dir=os.path.expanduser('~/.emailer')):
  creds = _get_or_create_creds(config_dir)
  return googleapiclient.discovery.build('gmail', 'v1', credentials=creds)


def authorize_sheets(config_dir=os.path.expanduser('~/.emailer')):
  creds = _get_or_create_creds(config_dir)
  return googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
