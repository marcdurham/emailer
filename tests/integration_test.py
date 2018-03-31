#!/usr/bin/env python3
'''
Unit tests.
Runs all the tests for this module.
'''

import collections
import datetime
import unittest

from emailer import data, main, models, utils


DEFAULT_URL = 'https://docs.google.com/spreadsheets/d/165AL8z-z5MlMrLyOEY8yJbNbLcqcKAcdvSeo-D5GSLE/edit'
DEFAULT_KEY = '165AL8z-z5MlMrLyOEY8yJbNbLcqcKAcdvSeo-D5GSLE'

class TestDataInterface(unittest.TestCase):
    '''Ensures that the data interface returns well-formatted data.'''

    @classmethod
    def setUpClass(cls):
        try:
            config = main.load_config()
            cls.gspread = data.GSpreadLoader(key=DEFAULT_KEY, auth=config['auth'])
        except Exception as e:
            print('Could not load the fixture spreadsheet. Try creating a '
                  'copy of the spreadsheet at ' + DEFAULT_URL + ' and sharing '
                  'it with the client_email address in your private.json '
                  "file. Don't forget to update your local.py with the new "
                  'URL.')
            raise e

    def test_fetch_people(self):
        self.people_test(self.gspread.fetch_people())

    def people_test(self, people):
        self.assertEqual(3, len(people))
        self.assertEqual('Test Two', people['T2'].name)
        self.assertEqual('2@t.ca', people['T2'].email)

    def test_fetch_groups(self):
        self.groups_test(self.gspread.fetch_groups())

    def groups_test(self, groups):
        self.assertEqual(3, len(groups))
        self.assertEqual(1, len(groups['one']))
        self.assertEqual(2, len(groups['two']))
        self.assertEqual(3, len(groups['all']))

    def test_fetch_templates(self):
        self.templates_test(self.gspread.fetch_templates())

    def templates_test(self, templates):
        self.assertEqual(3, len(templates))
        self.assertIn('Section2', templates)
        self.assertEqual('Wut {v3}', templates['Section2'])

    def date_verification_test(self, date_data, templates, correct_results):
        self.assertIn(data.CONTEXT, date_data)
        self.assertIn(data.SECTIONS, date_data)
        context = date_data[data.CONTEXT]
        for section_name in date_data[data.SECTIONS]:
            self.assertIn(section_name, templates)
            section = templates[section_name]
            self.assertEqual(
                correct_results[section_name],
                section.format_map(context))

    def test_fetch_dates_none(self):
        date = utils.parse_date('1111-11-11')
        date_data = self.gspread.fetch_date(date)
        self.assertIs(date_data, None)

    def test_fetch_dates_simple(self):
        date = utils.parse_date('1991-01-01')
        correct = {
            'Section1': '2 3',
            'Section2': 'Wut 4',
        }
        self.date_verification_test(
            self.gspread.fetch_date(date),
            self.gspread.fetch_templates(),
            correct)

    def test_fetch_dates_use_default(self):
        date = utils.parse_date('1991-01-02')
        correct = {
            'Section1': '5 2',
            'Section2': 'Wut 3',
            'Section3': 'Hi',
        }
        self.date_verification_test(
            self.gspread.fetch_date(date),
            self.gspread.fetch_templates(),
            correct)


if __name__ == '__main__':
    unittest.main()
