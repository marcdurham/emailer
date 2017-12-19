'''
Data API.
Current plans to support Google Spreadsheet only.
'''

import sys
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from . import models, utils

SECTIONS = 'sections'
CONTEXT = 'context'
DATE = 'date'
ID = 'ID'
DATE_FORMAT = '%d/%m/%Y'


class GSpreadLoader(object):
    def __init__(self, *, key, auth):
        self.key = key
        self.auth = auth
        try:
            self._authorize()
        except gspread.SpreadsheetNotFound:
            print('Config key "{}" was not found or is not a Spreadsheet ID.'.format(key))
            sys.exit(-1)
        except Exception as e:
            print('Exception: {}'.format(e))
            time.sleep(60)
            try:
                self._authorize()
            except Exception as e2:
                print('Another Exception: {}'.format(e))
                time.sleep(600)
                self._authorize()
        self.people_sheet = self.spreadsheet.worksheet('People')
        self.templates_sheet = self.spreadsheet.worksheet('Templates')
        self.sections_sheet = self.spreadsheet.worksheet('Sections')
        self.context_sheet = self.spreadsheet.worksheet('Context')
        self.people_data = self.people_sheet.get_all_values()
        self.templates_data = self.templates_sheet.get_all_values()
        self.sections_data = self.sections_sheet.get_all_values()
        self.context_data = self.context_sheet.get_all_records()

    def _authorize(self):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                self.auth, scope)
        self.client = gspread.authorize(credentials)
        self.spreadsheet = self.client.open_by_key(self.key)

    def parse_people_and_groups(self):
        self.people = {}
        A, B, C, *group_names = self.people_data[0]
        self.groups = {name: [] for name in group_names}
        self.group_map = {idx: name for idx, name in enumerate(group_names)}
        for i in range(1, len(self.people_data)):
            abbreviation, name, email, *groups = self.people_data[i]
            abbreviation = abbreviation.strip()
            person = models.Person(name=name, email=email)
            if abbreviation:
                self.people[abbreviation] = person
            else:
                self.people[name] = person
            for idx, value in enumerate(groups):
                if value:
                    group_name = self.group_map[idx]
                    if group_name.startswith('highlight-'):
                        person.highlights.append(value)
                    else:
                        self.groups[group_name].append(person)

    def parse_context_and_sections(self):
        self.default_context = utils.convert_empty_to_none(
            self.context_data[0])
        self.dates = {}
        context_by_id = {}
        for context in self.context_data[1:]:
            context_by_id[str(context[ID])] = utils.convert_empty_to_none(
                context)
        for entry in self.sections_data[1:]:
            date_string, context_id, *template_names = entry
            if date_string and context_id in context_by_id:
                date = utils.parse_date(date_string)
                context = context_by_id[context_id]
                sections = [name for name in template_names if name]
                self.dates[date] = {
                    SECTIONS: sections,
                    CONTEXT: context,
                    DATE: date,
                }

    def fetch_people(self):
        try:
            return self.people
        except AttributeError:
            self.parse_people_and_groups()
            return self.people

    def fetch_groups(self):
        try:
            return self.groups
        except AttributeError:
            self.parse_people_and_groups()
            return self.groups

    def fetch_templates(self):
        try:
            return self.templates
        except AttributeError:
            self.templates = {
                name.strip(): template.strip()
                for name, template, *rest in self.templates_data[1:]}
            return self.templates

    def fetch_default_context(self):
        try:
            return self.default_context
        except AttributeError:
            self.parse_context_and_sections()
            return self.default_context

    def fetch_date(self, date):
        try:
            return self.dates[date]
        except AttributeError:
            self.parse_context_and_sections()
            return self.fetch_date(date)
        except KeyError:
            return None