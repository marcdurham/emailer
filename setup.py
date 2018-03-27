#!/usr/bin/env python

import setuptools
import os

HERE = os.path.abspath(os.path.dirname(__file__))
README_MD = os.path.join(HERE, 'README.md')
README_RST = os.path.join(HERE, 'README.rst')
if os.path.exists(README_RST):
  readme_path = README_RST
else:
  readme_path = README_MD
with open(readme_path) as f:
  long_description = f.read()

setuptools.setup(
  name='emailer',
  version='0.3.3',
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
