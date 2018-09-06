import mistune


def convert(text):
  # Convert newlines to <br> with hard_wrap=True
  return mistune.markdown(text, hard_wrap=True)


def mark_text(text, highlights, values):
  for highlight in highlights:
    mark = values.get(highlight, highlight)
    text = text.replace(mark, f'<mark>{mark}</mark>')
  return text
