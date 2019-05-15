import logging
import time


def send_messages(messages, sender, skip, sleep=1):
  for message in messages:
    send_message(message=message, sender=sender, skip=skip)
    if sleep:
      time.sleep(sleep) # Avoids 500: Backend Error.


def send_message(*, message, sender, skip=False):
  if skip:
    return None
  logging.info(message)
  return sender.send(message)
