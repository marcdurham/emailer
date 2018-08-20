import base64
import httplib2
import json
import os.path

import googleapiclient.discovery
import google.oauth2.credentials
import google_auth_oauthlib.flow

from message import Message
from recipient import Recipient


def authorize(config_dir):
  scopes = [
      'https://www.googleapis.com/auth/gmail.send',
      'https://www.googleapis.com/auth/spreadsheets.readonly',
  ]
  creds_path = os.path.join(config_dir, 'client_secret.json')
  token_path = os.path.join(config_dir, 'token.json')
  if not os.path.exists(token_path):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        creds_path, scopes=scopes, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    auth_url, _ = flow.authorization_url(
        access_type='offline', prompt='consent')
    print('Please go to this URL: {}'.format(auth_url))
    code = input('Enter the authorization code: ')
    flow.fetch_token(code=code)
    credentials = flow.credentials
    with open(token_path, 'w') as token_file:
      json.dump({
          'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes
          }, token_file)
  with open(token_path, 'r') as token_file:
    creds = google.oauth2.credentials.Credentials(**json.load(token_file))
  gmail = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
  sheets = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
  message = Message(subject='Test', recipient=Recipient('P', 'weinan.wen@gmail.com'), body='<strong>Hi</strong>')
  body = {'raw': base64.urlsafe_b64encode(message.email_message.as_bytes()).decode()}
  message = (gmail.users().messages().send(
      userId='me', body=body)
      .execute())
  pprint(message)
  return gmail, sheets

if __name__ == '__main__':
  authorize(os.path.expanduser('~/.emailer'))
