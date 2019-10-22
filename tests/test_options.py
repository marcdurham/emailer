import logging

from emailer.options import Options


def test_returns_cmdline_value_if_no_method_defined(stub):
  options = Options(stub(a='hello'))
  assert options.a == 'hello'


def test_group_yields_whichever_group_is_passed(stub):
  assert Options(stub(active=1)).group == 'active'
  assert Options(stub(dryrun=1)).group == 'dryrun'
  assert Options(stub(test=1)).group == 'test'
  assert Options(stub()).group is None  # Perhaps an exception is better here.


def test_send_date_is_the_same_as_date(stub):
  options = Options(stub(date='2018-04-05', active=1))
  assert options.send_date == '2018-04-05'


def test_get_date_returns_one_day_later_for_dryrun_group(stub):
  options = Options(stub(date='2018-04-05', dryrun=1))
  assert options.send_date == '2018-04-06'


def test_log_level_returns_info_for_verbose_warn_by_default(stub):
  assert Options(stub(verbose=True)).log_level == logging.INFO
  assert Options(stub()).log_level == logging.WARNING
