from emailer import markdown


def test_markdown_converts_within_span():
  assert 'strong' in markdown.convert('<span>**a**</span>')


def test_markdown_converts_newline_to_br():
  assert '<br>' not in markdown.convert('a b')
  assert '<br>' in markdown.convert('a\nb')


def test_markdown_converts_vertical_pipes_to_table_without_header():
  assert '<table>' in markdown.convert('a|b')
  assert '<table>' in markdown.convert('#Hi\na|b')
  assert '<thead>' not in markdown.convert('a|b')


def test_markdown_converts_highlights():
  assert 'color' in markdown.convert('<<a>>')
  assert 'color' not in markdown.convert('<a>')


def test_markdown_converts_parses_highlights_inline():
  assert 'strong' not in markdown.convert('<<b>>')
  assert 'strong' in markdown.convert('<<**b**>>')


def test_mark_text_respects_word_boundaries():
  assert markdown.mark_text('a', ['a', 'n'], {}).count('>>') == 1


def test_mark_text_ignores_star_and_underscore():
  assert '<<' in markdown.mark_text('__a__', ['__a__'], {})
  assert '<<' in markdown.mark_text('**a**', ['**a**'], {})


def test_mark_text_only_highlights_unique_entries():
  highlighted = markdown.mark_text('A', ['A', 'A'], {})
  assert highlighted.count('>>') == 1


def test_mark_text_puts_mark_tags_around_text():
  assert '<<' not in markdown.mark_text('b', [''], {})
  assert '<<' not in markdown.mark_text('', ['b'], {})
  assert '<<' in markdown.mark_text('b', ['b'], {})


def test_mark_text_puts_mark_tags_around_substituted_text():
  assert '<<' in markdown.mark_text('a', ['T'], {'T': 'a'})
