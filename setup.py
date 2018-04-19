#!/usr/bin/env python

import emailer
import os
import setuptools


with open('README.md') as f:
  long_description = f.read()


setuptools.setup(
  name='emailer',
  version=emailer.__version__,
  description=emailer.__description__,
  long_description=long_description,
  long_description_content_type='text/markdown',
  url=emailer.__url__,
  author=emailer.__author__,
  author_email=emailer.__author_email__,
  license=emailer.__license__,
  packages=['emailer'],
  python_requires='>=3',
  include_package_data=True,
  install_requires=[
    'gspread',
    'oauth2client',
    'premailer',
    'PyYAML',
    'python-dateutil',
    'requests',
  ],
  entry_points={
    'console_scripts': [
      'email = emailer.main:main',
    ]
  },
)
