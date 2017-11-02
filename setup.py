#!/usr/bin/env python

from setuptools import setup
from os import path

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md')) as f:
  long_description = f.read()

setup(
  name='emailer',
  version='0.2.2',
  description='Send scheduled emails',
  long_description=long_description,
  url='https://github.com/WhiteHalmos/emailer',
  author='Peter Wen',
  author_email='peter@whitehalmos.org',
  license='MIT',
  packages=['emailer'],
  python_requires='>=3',
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
