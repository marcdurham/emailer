#!/usr/bin/env python3
'''
Unit tests.
Runs all the tests for this module.
'''

import collections
import datetime
import unittest

import data
import models
import utils
from local import URL


DEFAULT_URL = 'https://docs.google.com/spreadsheets/d/165AL8z-z5MlMrLyOEY8yJbNbLcqcKAcdvSeo-D5GSLE/edit'

class TestDataInterface(unittest.TestCase):
    '''Ensures that the data interface returns well-formatted data.'''

    @classmethod
    def setUpClass(cls):
        try:
            cls.yaml = data.YAMLLoader()
            url = DEFAULT_URL
            if URL:
                url = URL
            cls.gspread = data.GSpreadLoader(url=url)
        except Exception as e:
            print('Could not load the fixture spreadsheet. Try creating a '
                  'copy of the spreadsheet at ' + DEFAULT_URL + ' and sharing '
                  'it with the client_email address in your private.json '
                  "file. Don't forget to update your local.py with the new "
                  'URL.')
            raise e

    def test_fetch_people(self):
        self.people_test(self.yaml.fetch_people())
        self.people_test(self.gspread.fetch_people())

    def people_test(self, people):
        self.assertEqual(3, len(people))
        self.assertEqual('Test Two', people['T2'].name)
        self.assertEqual('2@t.ca', people['T2'].email)

    def test_fetch_groups(self):
        self.groups_test(self.yaml.fetch_groups())
        self.groups_test(self.gspread.fetch_groups())

    def groups_test(self, groups):
        self.assertEqual(3, len(groups))
        self.assertEqual(1, len(groups['one']))
        self.assertEqual(2, len(groups['two']))
        self.assertEqual(3, len(groups['all']))

    def test_fetch_templates(self):
        self.templates_test(self.yaml.fetch_templates())
        self.templates_test(self.gspread.fetch_templates())

    def templates_test(self, templates):
        self.assertEqual(3, len(templates))
        self.assertIn('Section2', templates)
        self.assertEqual('Wut {v3}', templates['Section2'])

    def test_fetch_default_context(self):
        self.default_context_test(self.yaml.fetch_default_context())
        self.default_context_test(self.gspread.fetch_default_context())

    def default_context_test(self, default_context):
        self.assertIn('v2', default_context)
        self.assertEqual(2, default_context['v2'])

    def date_verification_test(self, date_data, templates, default_context,
                               correct_results):
        self.assertIn(data.CONTEXT, date_data)
        self.assertIn(data.SECTIONS, date_data)
        for name in date_data[data.CONTEXT]:
            self.assertIn(name, default_context)
        context = default_context.copy()
        utils.update_if_not_none(context, date_data[data.CONTEXT])
        for section_name in date_data[data.SECTIONS]:
            self.assertIn(section_name, templates)
            section = templates[section_name]
            self.assertEqual(
                correct_results[section_name],
                section.format_map(context))

    def test_fetch_dates_none(self):
        date = utils.parse_date('1111-11-11')
        date_data = self.yaml.fetch_date(date)
        self.assertIs(date_data, None)
        date_data = self.gspread.fetch_date(date)
        self.assertIs(date_data, None)

    def test_fetch_dates_simple(self):
        date = utils.parse_date('1991-01-01')
        correct = {
            'Section1': '2 3',
            'Section2': 'Wut 4',
        }
        self.date_verification_test(
            self.yaml.fetch_date(date),
            self.yaml.fetch_templates(),
            self.yaml.fetch_default_context(),
            correct)
        self.date_verification_test(
            self.gspread.fetch_date(date),
            self.gspread.fetch_templates(),
            self.gspread.fetch_default_context(),
            correct)

    def test_fetch_dates_use_default(self):
        date = utils.parse_date('1991-01-02')
        correct = {
            'Section1': '5 2',
            'Section2': 'Wut 3',
            'Section3': 'Hi',
        }
        self.date_verification_test(
            self.yaml.fetch_date(date),
            self.yaml.fetch_templates(),
            self.yaml.fetch_default_context(),
            correct)
        self.date_verification_test(
            self.gspread.fetch_date(date),
            self.gspread.fetch_templates(),
            self.gspread.fetch_default_context(),
            correct)


class TestModels(unittest.TestCase):
    def test_create_person(self):
        name, email = 'Name', 'Email@Domain'
        person = models.Person.create([name, email])
        self.assertEqual(name, person.name)
        self.assertEqual(email, person.email)


class TestUtils(unittest.TestCase):
    def test_update_if_not_none(self):
        dict1 = {'1': 1, '2': 2}
        dict2 = {'1': None, '2': 3}
        utils.update_if_not_none(dict1, dict2)
        self.assertEqual(1, dict1['1'])
        self.assertEqual(3, dict1['2'])


if __name__ == '__main__':
    unittest.main()
