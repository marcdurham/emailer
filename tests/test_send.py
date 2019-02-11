from emailer.send import send_message


def test_send_sends_message(stub):
  sender = stub(send=lambda msg: 'b')
  assert send_message(message='a', sender=sender) == 'b'


def test_skips_sending_when_skip_is_true():
  assert send_message(message='a', sender=None, skip=True) is None
