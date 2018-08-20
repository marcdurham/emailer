def send_message(message, gmail):
  # https://developers.google.com/gmail/api/v1/reference/users/messages/send
  request = gmail.users().messages().send(userId='me', body=message.gmail_body)
  request.execute()


def send_messages(messages, gmail):
  for message in messages:
    send_message(message, gmail)
