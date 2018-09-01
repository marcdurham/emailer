def values(key, sheets):
  res = {}
  metadata = sheets.spreadsheets().get(
      spreadsheetId=key, fields='sheets.properties.title').execute()
  for prop in metadata['sheets']:
    title = prop['properties']['title']
    sheet_data = sheets.spreadsheets().values().get(
        spreadsheetId=key,
        range=title,
        fields='values',
        valueRenderOption='FORMATTED_VALUE').execute()
    # Use get in case there is no data on this sheet.
    res[title] = sheet_data.get('values')
  return res
