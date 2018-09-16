import pytest


@pytest.fixture(scope='session')
def stub():
  class Stub():
    def __init__(self, **kwargs):
      self.__dict__ = kwargs
  return Stub
