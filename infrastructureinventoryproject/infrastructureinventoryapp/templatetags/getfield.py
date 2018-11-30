# app/templatetags/getattribute.py

import re
from django import template
from ..models import APPLICATION_SERVER_FIELDS
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getfield(field):
    """Gets an attribute of an object dynamically from a string name"""
    for application_server_field in APPLICATION_SERVER_FIELDS:
        if application_server_field[0] == field:
            return application_server_field[1]
    return None



register.filter('getfield', getfield)