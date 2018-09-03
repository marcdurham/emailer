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


def substitute_for_key(key, values):
  return recursively_replace(values.get(key, ''), values)


def replace_value(values):
  return {k: values.get(v, v) for k, v in values.items()}
