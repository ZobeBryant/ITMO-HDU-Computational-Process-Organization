from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect

from fz_cli.utils import inspectutils
import six


VALUE_TYPES = (bool, six.string_types, six.integer_types, float, complex,
               type(Ellipsis), type(None), type(NotImplemented))


def IsGroup(component):
  return not IsCommand(component) and not IsValue(component)


def IsCommand(component):
  return inspect.isroutine(component) or inspect.isclass(component)


def IsValue(component):
  return isinstance(component, VALUE_TYPES) or HasCustomStr(component)


def IsSimpleGroup(component):

  assert isinstance(component, dict)
  for unused_key, value in component.items():
    if not IsValue(value) and not isinstance(value, (list, dict)):
      return False
  return True


def HasCustomStr(component):

  if hasattr(component, '__str__'):
    class_attrs = inspectutils.GetClassAttrsDict(type(component)) or {}
    str_attr = class_attrs.get('__str__')
    if str_attr and str_attr.defining_class is not object:
      return True
  return False
