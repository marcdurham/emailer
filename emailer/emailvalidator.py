def is_email_valid(email):
  if not '@' in email:
    return False
  name, domain = email.split('@', 1)
  if not name:
    return False
  return '.' in domain
