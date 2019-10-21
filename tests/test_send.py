from emailer import send


def test_send_sends_message(stub):
  sender = stub(send=lambda msg: 'b')
  assert send.send_message(message='a', sender=sender) == 'b'


def test_send_multiple_message(stub):
  counter = 0

  def mock_sender(_):
    nonlocal counter
    counter += 1
  sender = stub(send=mock_sender)

  messages = ['a', 'b', 'c']
  send.send_messages(messages, sender=sender, sleep=0.001)
  assert counter == 3
