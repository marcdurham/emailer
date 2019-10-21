import logging
import time


def send_messages(messages, sender, sleep=1):
  for message in messages:
    send_message(message=message, sender=sender)
    if sleep:
      time.sleep(sleep) # Avoids 500: Backend Error.


def send_message(*, message, sender):
  logging.info(message)
  return sender.send(message)
