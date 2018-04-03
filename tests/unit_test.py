#!/usr/bin/env python
'''
Unit tests.
Runs all the tests for this module.
'''

import unittest

from emailer import models, utils


class TestModels(unittest.TestCase):
  @staticmethod
  def _create_person():
    return models.Person.create(['1', '1@m'])

  def test_create_person(self):
    name, email = 'Name', 'Email@Domain'
    person = models.Person.create([name, email])
    self.assertEqual(name, person.name)
    self.assertEqual(email, person.email)

  def test_get_message(self):
    message = models.Message()
    message.sender = self._create_person()
    message.recipient = self._create_person()
    message.html = ''
    message.get_message()


class TestUtils(unittest.TestCase):
  def test_merge_with_default(self):
    dict1 = {'1': None, '2': 3}
    defaults = {'1': 1, '2': 2}
    result = utils.merge_with_default(dict1, defaults)
    self.assertEqual(1, result['1'])
    self.assertEqual(3, result['2'])


if __name__ == '__main__':
  unittest.main()
