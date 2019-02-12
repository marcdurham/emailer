import logging

def send_message(*, message, sender, skip=False):
  if skip:
    return None
  logging.info(message)
  return sender.send(message)
