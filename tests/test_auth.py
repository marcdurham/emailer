import pytest
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

from emailer import auth


@pytest.fixture
def creds_dict():
  return {
      'token': '1',
      'refresh_token': '2',
      'token_uri': '3',
      'client_id': '4',
      'client_secret': '5',
      'scopes': '6',
  }


def test_fetch_new_creds_calls_right_api(monkeypatch, stub):
  def myfrom(config, scopes):
    return stub(run_console=lambda: (config, scopes))
  monkeypatch.setattr(InstalledAppFlow, 'from_client_config', myfrom)
  creds = auth.fetch_new_creds({'hi': 'bye'})
  config, scopes = creds  # pylint: disable=unpacking-non-sequence
  assert config == {'hi': 'bye'}
  assert 'https://www.googleapis.com/auth/gmail.send' in scopes
  assert 'https://www.googleapis.com/auth/spreadsheets.readonly' in scopes


def test_serialize_creds_returns_dict(stub, creds_dict):
  creds = stub(**creds_dict)
  assert auth.serialize(creds) == creds_dict


def test_creds_fetches_new_creds_when_passed_none_or_empty_dict(monkeypatch):
  monkeypatch.setattr(auth, 'fetch_new_creds', lambda x: 'new' + x)
  assert auth.creds(None, 'config') == 'newconfig'
  assert auth.creds({}, 'config') == 'newconfig'


def test_creds_returns_deserialized_creds_when_passed_dict(creds_dict):
  creds = auth.creds(creds_dict)
  assert isinstance(creds, Credentials)
  for key, value in creds_dict.items():
    assert getattr(creds, key) == value
