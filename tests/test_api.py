import googleapiclient.discovery

from emailer import api


def test_services_using_correct_values_and_passes_in_creds(monkeypatch):
  def mybuild(service, version, credentials, **_):
    return (service, version, credentials)
  monkeypatch.setattr(googleapiclient.discovery, 'build', mybuild)
  assert api.gmail('creds') == ('gmail', 'v1', 'creds')
  assert api.sheets('creds2') == ('sheets', 'v4', 'creds2')
