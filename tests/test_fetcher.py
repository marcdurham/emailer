import pytest

from emailer import fetcher


@pytest.fixture
def sheets(stub):
  # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get
  # pylint: disable=bad-continuation
  return lambda metadata, data: stub(spreadsheets=lambda: stub(
      get=lambda spreadsheetId, fields: stub(execute=lambda: metadata),
      values=lambda: stub(get=lambda spreadsheetId, range, fields,
                          valueRenderOption: stub(execute=lambda: data[range])))
                                     )


# pylint: disable=redefined-outer-name
def test_fetch_correct_sheets_and_data(sheets):
  metadata = {
      'sheets': [{
          'properties': {
              'title': 'Sheet1'
          }
      }, {
          'properties': {
              'title': 'Sheet2'
          }
      }]
  }
  sheet1_vals = [['S1A1', 'S1B1'], ['S1A2', 'S1B2']]
  sheet2_vals = [['S2A1', 'S2B1'], ['S2A2', 'S2B2']]
  data = {'Sheet1': {'values': sheet1_vals}, 'Sheet2': {'values': sheet2_vals}}
  values = fetcher.values('any', sheets(metadata, data))
  assert values['Sheet1'] == sheet1_vals
  assert values['Sheet2'] == sheet2_vals
  assert len(values) == 2
