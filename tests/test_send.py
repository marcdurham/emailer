from emailer.send import send_messages


def test_sends_all_messages(stub):
  sender = stub(send=lambda *args: 1)
  assert send_messages(['a', 'b'], sender) == [1, 1]


def test_skips_sending_when_skip_is_true(stub):
  sender = stub(send=lambda *args: 1)
  assert send_messages(['a'], sender, skip=True) is None
