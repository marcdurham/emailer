import googleapiclient.discovery


def gmail(creds):
  # Workaround for import error: https://stackoverflow.com/a/44518587
  return googleapiclient.discovery.build(
      'gmail', 'v1', credentials=creds, cache_discovery=False)


def sheets(creds):
  return googleapiclient.discovery.build(
      'sheets', 'v4', credentials=creds, cache_discovery=False)
