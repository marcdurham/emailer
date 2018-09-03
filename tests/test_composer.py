from emailer import composer


def test_replace_replaces_names_with_values():
  assert composer.replace('{hi}', {'hi': 'bye'}) == 'bye'


def test_replace_leaves_undefined_template_names():
  assert composer.replace('{hi}', {}) == '{hi}'


def test_substitute_for_key_finds_text_by_key():
  assert composer.substitute_for_key('hi', {'hi': 't'}) == 't'


def test_replace_value_runs_once():
  assert composer.replace_value({'hi': 'T', 'T': 'a'}) == {'hi': 'a', 'T': 'a'}
