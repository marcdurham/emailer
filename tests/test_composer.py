from emailer import composer
from emailer.recipient import Recipient


def test_replace_replaces_names_with_values():
  assert composer.replace('$hi', {'hi': 'bye'}) == 'bye'


def test_replace_leaves_undefined_template_names():
  assert composer.replace('$hi', {}) == '$hi'


def test_substitute_for_key_finds_text_by_key():
  assert composer.substitute_for_key('hi', {'hi': 't'}) == 't'


def test_replace_values_runs_once():
  assert composer.replace_values({'h': 'T', 'T': 'a'}) == {'h': 'a', 'T': 'a'}


def test_markdown_replaces_newline_with_br():
  assert '<br>' not in composer.markdown('a b')
  assert '<br>' in composer.markdown('a\nb')


def test_mark_text_puts_mark_tags_around_text():
  assert composer.mark_text('a b c', 'b', {}) == 'a <mark>b</mark> c'


def test_mark_text_puts_mark_tags_around_substituted_text():
  assert composer.mark_text('a b c', 'T', {'T': 'a'}) == '<mark>a</mark> b c'


def test_get_prefix_for_group_adds_prefix_for_dryrun_and_test():
  assert composer.get_prefix_for_group('active') == ''
  assert 'DRYRUN' in composer.get_prefix_for_group('dryrun')
  assert 'TEST' in composer.get_prefix_for_group('test')


def test_get_replyto_returns_none_or_recipient():
  assert composer.get_replyto({}) is None
  assert composer.get_replyto({'replyto': 'a@b.com'}) == Recipient('a@b.com')