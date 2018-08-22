import json

from emailer import config


def test_load_tokens_fails_with_no_file(tmpdir):
  creds_file = tmpdir.join('creds.json')
