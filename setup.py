#!/usr/bin/env python

import emailer
import os
import setuptools


def get_long_description():
  HERE = os.path.abspath(os.path.dirname(__file__))
  README_MD = os.path.join(HERE, 'README.md')
  README_RST = os.path.join(HERE, 'README.rst')
  if os.path.exists(README_RST):
    readme_path = README_RST
  else:
    readme_path = README_MD
  with open(readme_path) as f:
    return f.read()


setuptools.setup(
  name='emailer',
  version=emailer.__version__,
  description=emailer.__description__,
  long_description=get_long_description(),
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
