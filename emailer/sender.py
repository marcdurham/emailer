import logging


def send_message(message, gmail, skip_send=False):
  if skip_send:
    logging.info('Skipped sending')
    return None
  logging.info('Sending %s', message)
  return gmail.users().messages().send(
      userId='me', body=message.gmail_body).execute()


def send_messages(messages, gmail, skip_send=False):
  return (send_message(m, gmail, skip_send) for m in messages)
