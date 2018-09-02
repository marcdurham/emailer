def replace(template, values):
  class Default(dict):
    def __missing__(self, key):
      return '{' + key + '}'
  return template.format_map(Default(values))


def recursively_replace(template, values):
  current_template = template
  last_template = None
  while current_template != last_template:
    last_template = current_template
    current_template = replace(current_template, values)
  return current_template


def compose_email_subject(email, shortcuts, markdown):
  values = {**email, **shortcuts, **markdown}
  subject = values.get('subject')
  if subject:
    return recursively_replace(subject, values)
  return None


# TODO: Refactor.
def compose_email_body(email, shortcuts, markdown):
  values = {**email, **shortcuts, **markdown}
  subject = values.get('body')
  if subject:
    return recursively_replace(subject, values)
  return None
