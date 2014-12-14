import re


def is_valid_tn(tn_string):
    valid_tn = re.compile('^\d{3}-\d{3}-\d{4}$')
    return re.match(valid_tn, tn_string)
