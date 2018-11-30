# app/templatetags/getattribute.py

import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    else:
        return None


register.filter('getattribute', getattribute)