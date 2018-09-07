import re

import mistune


def highlight_text(text, colour='yellow'):
  return f'<strong style="background-color: {colour}">{text}</strong>'


def mark_text(text, highlights, values):
  for highlight in highlights:
    mark = values.get(highlight, highlight)
    if mark:
      text = text.replace(mark, highlight_text(mark))
  return text


class SimpleTableBlockLexer(mistune.BlockLexer):
  def enable_simple_table(self):
    self.rules.simple_table = re.compile(
        r'((?:.*\|.*(?:\n|$))+)\n*')
    idx = self.default_rules.index('nptable')
    self.default_rules.insert(idx + 1, 'simple_table')

  def parse_simple_table(self, matches):
    cells = re.sub(r'\n$', '', matches.group(1))
    cells = cells.split('\n')
    for i, values in enumerate(cells):
      cells[i] = re.split(r' *(?<!\\)\| *', values)
    self.tokens.append({
        'type': 'simple_table',
        'cells': cells})


class SimpleTableMarkdown(mistune.Markdown):
  def output_simple_table(self):
    body = self.renderer.placeholder()
    for row in self.token['cells']:
      cell = self.renderer.placeholder()
      for value in row:
        cell += self.renderer.table_cell(
            self.inline(value), header=False, align=None)
      body += self.renderer.table_row(cell)
    return f'<table><tbody>{body}</tbody></table>\n'


def convert(text):
  block = SimpleTableBlockLexer(mistune.BlockGrammar())
  block.enable_simple_table()
  markdown = SimpleTableMarkdown(block=block, hard_wrap=True)
  return markdown(text)
