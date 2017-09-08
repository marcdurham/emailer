'''
Data API.
Current plans to support Google Spreadsheet and YAML.
'''

import os
import time

import gspread
import json
import yaml
from oauth2client.service_account import ServiceAccountCredentials

import models
import utils


SECTIONS = 'sections'
CONTEXT = 'context'
ID = 'ID'
DATE_FORMAT = '%d/%m/%Y'


class GSpreadLoader(object):

    def __init__(self, key=None, name=None, url=None):
        try:
            self._authorize()
        except Exception as e:
            print('Exception: {}'.format(e))
            print('Retrying in 1 minute')
            time.sleep(60)
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
        credentials = ServiceAccountCredentials.from_json_keyfile_name('private.json', scope)
        self.client = gspread.authorize(credentials)
        if key:
            self.spreadsheet = self.client.open_by_key(key)
        elif name:
            self.spreadsheet = self.client.open(name)
        elif url:
            self.spreadsheet = self.client.open_by_url(url)

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
                    if group_name == 'Highlight':
                        person.highlight = value
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
                for name, template in self.templates_data[1:]}
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


class YAMLLoader(object):

    def __init__(self, directory=None, people_file=None, templates_file=None,
                 dates_file=None, defaults_file=None):
        directory = directory or 'fixture'
        people_file = (
            people_file or os.path.join(directory, 'people.yml'))
        templates_file = (
            templates_file or os.path.join(directory, 'templates.yml'))
        dates_file = (
            dates_file or os.path.join(directory, 'dates.yml'))
        defaults_file = (
            defaults_file or os.path.join(directory, 'defaults.yml'))
        with open(people_file, 'r') as people_data_stream:
            self.people_data = yaml.load(people_data_stream)
        with open(templates_file, 'r') as templates_data_stream:
            self.templates_data = yaml.load(templates_data_stream)
        with open(dates_file, 'r') as dates_data_stream:
            self.dates_data = yaml.load(dates_data_stream)
        with open(defaults_file, 'r') as defaults_data_stream:
            self.defaults_data = yaml.load(defaults_data_stream)

    def fetch_date(self, date):
        try:
            return self.dates_data[date]
        except KeyError:
            return None

    def fetch_default_context(self):
        return self.defaults_data

    def fetch_templates(self):
        return self.templates_data

    def fetch_groups(self):
        try:
            return self.groups
        except AttributeError:
            people = self.fetch_people()
            self.groups = {}
            def fill_group(name, abbreviation_list):
                group = []
                for abbreviation in abbreviation_list:
                    assert abbreviation in people, (
                        'No abbreviation {} for group {}'.format(
                            abbreviation, name))
                    group.append(people[abbreviation])
                return group

            for name, abbreviation_list in self.people_data['groups'].items():
                if abbreviation_list is None:
                    self.groups[name] = list(people.values())
                else:
                    self.groups[name] = fill_group(name, abbreviation_list)
            return self.groups

    def fetch_people(self):
        try:
            return self.people
        except AttributeError:
            self.people = {}
            people_dict = self.people_data['people']
            for abbreviation, person_data in people_dict.items():
                person = models.Person.create(person_data)
                self.people[abbreviation] = person
            return self.people
