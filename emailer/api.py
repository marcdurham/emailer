import googleapiclient.discovery


def gmail(creds):
  return googleapiclient.discovery.build('gmail', 'v1', credentials=creds)


def sheets(creds):
  return googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
