from collections import Counter

import pytest

from emailer import __main__ as main, args as args_mod, shell


@pytest.fixture
def main_spies(monkeypatch):
  counter = Counter()

  def spy_get_version():
    nonlocal counter
    counter.update(('get_version', 1))
    return 'testing get version'

  def spy_get_sample_config():
    nonlocal counter
    counter.update(('get_sample_config', 1))
    return 'testing get sample config'

  # pylint: disable=too-many-arguments, unused-argument
  def spy_process_sheets(group,
                         config_dir,
                         key_names,
                         all_keys,
                         date,
                         skip):
    nonlocal counter
    counter.update(('process_sheets', 1))

  monkeypatch.setattr(main, 'get_version', spy_get_version)
  monkeypatch.setattr(main, 'get_sample_config', spy_get_sample_config)
  monkeypatch.setattr(shell, 'process_sheets', spy_process_sheets)
  return counter


# pylint: disable=redefined-outer-name
def test_main_version(main_spies, monkeypatch):
  args = args_mod.get_parsed_args(['--version'])
  monkeypatch.setattr(main, 'get_parsed_args', lambda: args)
  main.main()
  assert (main_spies['get_version']) == 1
  assert (main_spies['get_sample_config']) == 0
  assert (main_spies['process_sheets']) == 0


# pylint: disable=redefined-outer-name
def test_main_sample_config(main_spies, monkeypatch):
  args = args_mod.get_parsed_args(['--sample-config'])
  monkeypatch.setattr(main, 'get_parsed_args', lambda: args)
  main.main()
  assert (main_spies['get_version']) == 0
  assert (main_spies['get_sample_config']) == 1
  assert (main_spies['process_sheets']) == 0


# pylint: disable=redefined-outer-name
def test_main(main_spies, monkeypatch, capsys):
  args = args_mod.get_parsed_args(['--skip-send'])
  monkeypatch.setattr(main, 'get_parsed_args', lambda: args)
  main.main()
  assert (main_spies['get_version']) == 0
  assert (main_spies['get_sample_config']) == 0
  assert (main_spies['process_sheets']) == 0
  out, err = capsys.readouterr()
  assert out == 'No group provided\n'
  assert err == ''


# pylint: disable=redefined-outer-name
def test_main_no_group(main_spies, monkeypatch):
  args = args_mod.get_parsed_args(['--skip-send', '--test'])
  monkeypatch.setattr(main, 'get_parsed_args', lambda: args)
  main.main()
  assert (main_spies['get_version']) == 0
  assert (main_spies['get_sample_config']) == 0
  assert (main_spies['process_sheets']) == 1
