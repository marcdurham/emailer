'''
Various standalone utility functions
'''

import dateutil.parser


def parse_date(date_string):
    return dateutil.parser.parse(date_string, dayfirst=True).date()


def convert_empty_to_none(dictionary):
    new_dict = {}
    for name, value in dictionary.items():
        if value == '':
            new_dict[name] = None
        else:
            new_dict[name] = value
    return new_dict


def update_if_not_none(dict1, dict2):
    '''
    Updates dict1 by dict2's (key, value) pair if and only if dic2's value
    is not None.
    '''
    for key, value in dict2.items():
        if value is not None:
            dict1[key] = value
