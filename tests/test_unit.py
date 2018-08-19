#!/usr/bin/env python
'''
Unit tests.
Runs all the tests for this module.
'''

import unittest

from .context import emailer


class TestModels(unittest.TestCase):
  @staticmethod
  def _create_person():
    return models.Person('1', '1@m')

  def test_create_person(self):
    name, email = 'Name', 'Email@Domain'
    person = models.Person(name, email)
    self.assertEqual(name, person.name)
    self.assertEqual(models.Email(email), person.email)

  def test_get_message(self):
    msg = models.Message(
        sender = models.Person('1', '2@3'),
        recipient = models.Person('2', '3@4'),
        subject = 'ba',
        html = 'hi')
    msg.get_message()


class TestUtils(unittest.TestCase):
  def test_merge_with_default(self):
    dict1 = {'1': None, '2': 3}
    defaults = {'1': 1, '2': 2}
    result = utils.merge_with_default(dict1, defaults)
    self.assertEqual(1, result['1'])
    self.assertEqual(3, result['2'])


if __name__ == '__main__':
  unittest.main()
