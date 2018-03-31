#!/usr/bin/env python3
'''
Unit tests.
Runs all the tests for this module.
'''

import collections
import datetime
import unittest

from emailer import data, main, models, utils


class TestModels(unittest.TestCase):
    def test_create_person(self):
        name, email = 'Name', 'Email@Domain'
        person = models.Person.create([name, email])
        self.assertEqual(name, person.name)
        self.assertEqual(email, person.email)


class TestUtils(unittest.TestCase):
    def test_merge_with_default(self):
        dict1 = {'1': None, '2': 3}
        defaults = {'1': 1, '2': 2}
        result = utils.merge_with_default(dict1, defaults)
        self.assertEqual(1, result['1'])
        self.assertEqual(3, result['2'])


if __name__ == '__main__':
    unittest.main()
