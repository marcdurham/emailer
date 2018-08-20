def fetch_values(key, sheets):
  res = {}
  '''
  {'sheets': [{'properties': {'title': 'Context'}},
              {'properties': {'title': 'People'}},
              {'properties': {'title': 'Templates'}}]}
  '''
  metadata = sheets.spreadsheets().get(
      spreadsheetId=key, fields='sheets.properties.title').execute()
  for prop in metadata['sheets']:
    title = prop['properties']['title']
    '''
    {'values': [['A1',
                 'B1'],
                ['A2',
                 'B2'],
                ...]}
    '''
    data = sheets.spreadsheets().values().get(
        spreadsheetId=key,
        range=title,
        fields='values',
        valueRenderOption='FORMATTED_VALUE').execute()
    res[title] = data['values']
  return res
