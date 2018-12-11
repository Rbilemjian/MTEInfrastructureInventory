# app/templatetags/getattribute.py

import re
from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe

numeric_test = re.compile("^\d+$")
register = template.Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(serialize('json', [object]))


register.filter('jsonify', jsonify)
