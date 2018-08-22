def send_message(message, gmail):
  return gmail.users().messages().send(
      userId='me', body=message.gmail_body).execute()


def send_messages(messages, gmail):
  return [send_message(m, gmail) for m in messages]
