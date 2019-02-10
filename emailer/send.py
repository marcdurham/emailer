def send_messages(messages, sender, skip=False):
  if skip:
    return None
  return [sender.send(m) for m in messages]
