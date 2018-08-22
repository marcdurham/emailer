import pretend
import pytest


@pytest.fixture(scope='session')
def stub():
  return pretend.stub
