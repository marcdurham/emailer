#!/usr/bin/env python

import emailer.models
import emailer.utils


def test_create_person():
  name, email = 'Name', 'Email@Domain'
  person = emailer.models.Person(name, email)
  assert person.name == name
  assert person.email == email


def test_merge_with_default_replaces_none_with_default():
  result = emailer.utils.merge_with_default({1: None}, {1: 2})
  assert result[1] == 2
