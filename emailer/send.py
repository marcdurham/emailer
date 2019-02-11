def send_message(*, message, sender, skip=False):
  if skip:
    return None
  return sender.send(message)
