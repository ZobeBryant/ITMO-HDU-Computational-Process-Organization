
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import sys
import types

from fz_cli.utils import docstrings

import six


class FullArgSpec(object):

  def __init__(self, args=None, varargs=None, varkw=None, defaults=None,
               kwonlyargs=None, kwonlydefaults=None, annotations=None):
    self.args = args or []
    self.varargs = varargs
    self.varkw = varkw
    self.defaults = defaults or ()
    self.kwonlyargs = kwonlyargs or []
    self.kwonlydefaults = kwonlydefaults or {}
    self.annotations = annotations or {}


def _GetArgSpecInfo(fn):
  skip_arg = False
  if inspect.isclass(fn):
    # If the function is a class, we try to use its init method.
    skip_arg = True
    if six.PY2 and hasattr(fn, '__init__'):
      fn = fn.__init__
  elif inspect.ismethod(fn):
    # If the function is a bound method, we skip the `self` argument.
    skip_arg = fn.__self__ is not None
  elif inspect.isbuiltin(fn):
    # If the function is a bound builtin, we skip the `self` argument, unless
    # the function is from a standard library module in which case its __self__
    # attribute is that module.
    if not isinstance(fn.__self__, types.ModuleType):
      skip_arg = True
  elif not inspect.isfunction(fn):
    # The purpose of this else clause is to set skip_arg for callable objects.
    skip_arg = True
  return fn, skip_arg


def Py2GetArgSpec(fn):
  """A wrapper around getargspec that tries both fn and fn.__call__."""
  try:
    return inspect.getargspec(fn)  # pylint: disable=deprecated-method
  except TypeError:
    if hasattr(fn, '__call__'):
      return inspect.getargspec(fn.__call__)  # pylint: disable=deprecated-method
    raise


def Py3GetFullArgSpec(fn):
  try:
    sig = inspect._signature_from_callable(  # pylint: disable=protected-access
        fn,
        skip_bound_arg=True,
        follow_wrapper_chains=True,
        sigcls=inspect.Signature)
  except Exception:
    # 'signature' can raise ValueError (most common), AttributeError, and
    # possibly others. We catch all exceptions here, and reraise a TypeError.
    raise TypeError('Unsupported callable.')

  args = []
  varargs = None
  varkw = None
  kwonlyargs = []
  defaults = ()
  annotations = {}
  defaults = ()
  kwdefaults = {}

  if sig.return_annotation is not sig.empty:
    annotations['return'] = sig.return_annotation

  for param in sig.parameters.values():
    kind = param.kind
    name = param.name

    # pylint: disable=protected-access
    if kind is inspect._POSITIONAL_ONLY:
      args.append(name)
    elif kind is  inspect._POSITIONAL_OR_KEYWORD:
      args.append(name)
      if param.default is not param.empty:
        defaults += (param.default,)
    elif kind is  inspect._VAR_POSITIONAL:
      varargs = name
    elif kind is  inspect._KEYWORD_ONLY:
      kwonlyargs.append(name)
      if param.default is not param.empty:
        kwdefaults[name] = param.default
    elif kind is  inspect._VAR_KEYWORD:
      varkw = name
    if param.annotation is not param.empty:
      annotations[name] = param.annotation
    # pylint: enable=protected-access

  if not kwdefaults:
    # compatibility with 'func.__kwdefaults__'
    kwdefaults = None

  if not defaults:
    # compatibility with 'func.__defaults__'
    defaults = None
  return inspect.FullArgSpec(args, varargs, varkw, defaults,
                             kwonlyargs, kwdefaults, annotations)
  # pylint: enable=no-member
  # pytype: enable=module-attr


def GetFullArgSpec(fn):
  """Returns a FullArgSpec describing the given callable."""
  original_fn = fn
  fn, skip_arg = _GetArgSpecInfo(fn)

  try:
    if sys.version_info[0:2] >= (3, 5):
      (args, varargs, varkw, defaults,
       kwonlyargs, kwonlydefaults, annotations) = Py3GetFullArgSpec(fn)
    elif six.PY3:  # Specifically Python 3.4.
      (args, varargs, varkw, defaults,
       kwonlyargs, kwonlydefaults, annotations) = inspect.getfullargspec(fn)  # pylint: disable=deprecated-method,no-member
    else:  # six.PY2
      args, varargs, varkw, defaults = Py2GetArgSpec(fn)
      kwonlyargs = kwonlydefaults = None
      annotations = getattr(fn, '__annotations__', None)

  except TypeError:

    if inspect.isbuiltin(fn):
      return FullArgSpec(varargs='vars', varkw='kwargs')

    fields = getattr(original_fn, '_fields', None)
    if fields is not None:
      return FullArgSpec(args=list(fields))


    return FullArgSpec()

  skip_arg_required = six.PY2 or sys.version_info[0:2] == (3, 4)
  if skip_arg_required and skip_arg and args:
    args.pop(0)  # Remove 'self' or 'cls' from the list of arguments.
  return FullArgSpec(args, varargs, varkw, defaults,
                     kwonlyargs, kwonlydefaults, annotations)


def GetFileAndLine(component):
  if inspect.isbuiltin(component):
    return None, None

  try:
    filename = inspect.getsourcefile(component)
  except TypeError:
    return None, None

  try:
    unused_code, lineindex = inspect.findsource(component)
    lineno = lineindex + 1
  except IOError:
    lineno = None

  return filename, lineno


def Info(component):
  try:
    from IPython.core import oinspect
    inspector = oinspect.Inspector()
    info = inspector.info(component)
    if info['docstring'] == '<no docstring>':
      info['docstring'] = None
  except ImportError:
    info = _InfoBackup(component)

  try:
    unused_code, lineindex = inspect.findsource(component)
    info['line'] = lineindex + 1
  except (TypeError, IOError):
    info['line'] = None

  if 'docstring' in info:
    info['docstring_info'] = docstrings.parse(info['docstring'])

  return info


def _InfoBackup(component):
  info = {}

  info['type_name'] = type(component).__name__
  info['string_form'] = str(component)

  filename, lineno = GetFileAndLine(component)
  info['file'] = filename
  info['line'] = lineno
  info['docstring'] = inspect.getdoc(component)

  try:
    info['length'] = str(len(component))
  except (TypeError, AttributeError):
    pass

  return info


def IsNamedTuple(component):
  if not isinstance(component, tuple):
    return False

  has_fields = bool(getattr(component, '_fields', None))
  return has_fields


def GetClassAttrsDict(component):
  """Gets the attributes of the component class, as a dict with name keys."""
  if not inspect.isclass(component):
    return None
  class_attrs_list = inspect.classify_class_attrs(component)
  return {
      class_attr.name: class_attr
      for class_attr in class_attrs_list
  }
