from emailer import markdown


def test_markdown_converts_newline_to_br():
  assert '<br>' not in markdown.convert('a b')
  assert '<br>' in markdown.convert('a\nb')


def test_markdown_converts_vertical_pipes_to_table_without_header():
  assert '<table>' in markdown.convert('a|b')
  assert '<table>' in markdown.convert('#Hi\na|b')
  assert '<thead>' not in markdown.convert('a|b')


def test_mark_text_puts_mark_tags_around_text():
  assert 'color' not in markdown.mark_text('b', [''], {})
  assert 'color' not in markdown.mark_text('', ['b'], {})
  # No bold for highlights
  assert 'strong' not in markdown.mark_text('b', ['b'], {})
  assert 'color' in markdown.mark_text('b', ['b'], {})


def test_mark_text_puts_mark_tags_around_substituted_text():
  assert 'color' in markdown.mark_text('a', ['T'], {'T': 'a'})
