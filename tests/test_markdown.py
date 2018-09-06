from emailer import markdown


def test_markdown_replaces_newline_with_br():
  assert '<br>' not in markdown.convert('a b')
  assert '<br>' in markdown.convert('a\nb')


def test_mark_text_puts_mark_tags_around_text():
  assert markdown.mark_text('a b c', 'b', {}) == 'a <mark>b</mark> c'


def test_mark_text_puts_mark_tags_around_substituted_text():
  assert markdown.mark_text('a b c', 'T', {'T': 'a'}) == '<mark>a</mark> b c'
