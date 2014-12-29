import re


def is_valid_tn(tn_string, blank=False):
    valid_tn = False
    regex = re.compile('^\d{3}-\d{3}-\d{4}$')
    if re.match(regex, tn_string):
        valid_tn = True
    if blank and not valid_tn and tn_string == '':
        valid_tn = True
    return valid_tn
