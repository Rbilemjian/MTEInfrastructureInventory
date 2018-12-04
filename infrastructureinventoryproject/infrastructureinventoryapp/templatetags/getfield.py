# app/templatetags/getattribute.py

import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getfield(field, arg):
    """Gets an attribute of an object dynamically from a string name"""
    for model_field in arg:
        if model_field[0] == field:
            return model_field[1]
    return None



register.filter('getfield', getfield)