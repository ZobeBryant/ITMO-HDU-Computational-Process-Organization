
"""Python Fz is a library for creating CLIs from absolutely any Python object.

You can call Fz on any Python object:
functions, classes, modules, objects, lists, tuples, etc.

Python Fz turns any Python object into a command line interface.
Simply call the Fz function as your main method to create a CLI.

When using Fz to build a CLI, your main method includes a call to Fz. Eg:

def main(argv):
  fz_cli.fz(Component)

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import json
import re
import shlex
import sys
import types
import os
from fz_cli.utils import decorators, parser, inspectutils, value_types
from fz_cli import trace
import six



def Fz(component=None, command=None, name=None):
  """This function, Fz, is the main entrypoint for Python Fz.

  """
  name = name or os.path.basename(sys.argv[0])

  # Get args as a list.
  if isinstance(command, six.string_types):
    args = shlex.split(command)
  elif isinstance(command, (list, tuple)):
    args = command
  elif command is None:
    # Use the command line args by default if no command is specified.
    args = sys.argv[1:]
  else:
    raise ValueError('The command argument must be a string or a sequence of '
                     'arguments.')

  args, flag_args = parser.SeparateFlagArgs(args)

  argparser = parser.CreateParser()
  parsed_flag_args, unused_args = argparser.parse_known_args(flag_args)

  context = {}
  if component is None:
    # Determine the calling context.
    caller = inspect.stack()[1]
    caller_frame = caller[0]
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    context.update(caller_globals)
    context.update(caller_locals)

  component_trace = _Fz(component, args, parsed_flag_args, context, name)

  if component_trace.HasError():

    raise FzExit(2, component_trace)

  if component_trace.show_trace:
    output = ['Fz trace:\n{trace}'.format(trace=component_trace)]
    Display(output, out=sys.stderr)
    raise FzExit(0, component_trace)

  # The command succeeded normally; print the result.
  _PrintResult(component_trace, verbose=component_trace.verbose)
  result = component_trace.GetResult()
  return result


def Display(lines, out):
  text = '\n'.join(lines) + '\n'
  print(text)




class FzError(Exception):
  """Exception used by Fz when a Fz command cannot be executed.

  These exceptions are not raised by the Fz function, but rather are caught
  and added to the FzTrace.
  """


class FzExit(SystemExit):  # pylint: disable=g-bad-exception-name


  def __init__(self, code, component_trace):
    """Constructs a FzExit exception.

    Args:
      code: (int) Exit code for the Fz CLI.
      component_trace: (FzTrace) The trace for the Fz command.
    """
    super(FzExit, self).__init__(code)
    self.trace = component_trace





def _PrintResult(component_trace, verbose=False):
  """Prints the result of the Fz call to stdout in a human readable way."""
  result = component_trace.GetResult()

  if value_types.HasCustomStr(result):
    # If the object has a custom __str__ method, rather than one inherited from
    # object, then we use that to serialize the object.
    print(str(result))
    return

  if isinstance(result, (list, set, frozenset, types.GeneratorType)):
    for i in result:
      print(_OneLineResult(i))
  elif inspect.isgeneratorfunction(result):
    raise NotImplementedError
  elif isinstance(result, tuple):
    print(_OneLineResult(result))
  elif isinstance(result, value_types.VALUE_TYPES):
    if result is not None:
      print(result)





def _OneLineResult(result):
  if isinstance(result, six.string_types):
    return str(result).replace('\n', ' ')
  if inspect.isfunction(result):
    return '<function {name}>'.format(name=result.__name__)
  if inspect.ismodule(result):
    return '<module {name}>'.format(name=result.__name__)
  try:
    return json.dumps(result, ensure_ascii=False)
  except (TypeError, ValueError):
    return str(result).replace('\n', ' ')

def _Fz(component, args, parsed_flag_args, context, name=None):
  """Execute a FZ command on a target component using the args supplied.

  """
  verbose = parsed_flag_args.verbose
  separator = parsed_flag_args.separator
  show_help = parsed_flag_args.help
  show_trace = parsed_flag_args.trace

  # component can be a module, class, routine, object, etc.
  if component is None:
    component = context

  initial_component = component
  component_trace = trace.FzTrace(
      initial_component=initial_component, name=name, separator=separator,
      verbose=verbose, show_trace=show_trace)

  instance = None
  remaining_args = args
  while True:
    last_component = component
    initial_args = remaining_args
    saved_args = []
    used_separator = False
    if separator in remaining_args:
      # For the current component, only use arguments up to the separator.
      separator_index = remaining_args.index(separator)
      saved_args = remaining_args[separator_index + 1:]
      remaining_args = remaining_args[:separator_index]
      used_separator = True
    assert separator not in remaining_args

    handled = False
    candidate_errors = []

    is_callable = inspect.isclass(component) or inspect.isroutine(component)
    is_callable_object = callable(component) and not is_callable
    is_sequence = isinstance(component, (list, tuple))
    is_map = isinstance(component, dict) or inspectutils.IsNamedTuple(component)

    if not handled and is_callable:
      # The component is a class or a routine; we'll try to initialize it or
      # call it.
      is_class = inspect.isclass(component)

      try:
        component, remaining_args = _CallAndUpdateTrace(
            component,
            remaining_args,
            component_trace,
            treatment='class' if is_class else 'routine',
            target=component.__name__)
        handled = True
      except FzError as error:
        candidate_errors.append((error, initial_args))

      if handled and last_component is initial_component:
        # If the initial component is a class, keep an instance for use with -i.
        instance = component

    if not handled and is_sequence and remaining_args:
      # The component is a tuple or list; we'll try to access a member.
      arg = remaining_args[0]
      try:
        index = int(arg)
        component = component[index]
        handled = True
      except (ValueError, IndexError):
        error = FzError(
            'Unable to index into component with argument:', arg)
        candidate_errors.append((error, initial_args))

      if handled:
        remaining_args = remaining_args[1:]
        filename = None
        lineno = None
        component_trace.AddAccessedProperty(
            component, index, [arg], filename, lineno)

    if not handled and is_map and remaining_args:
      # The component is a dict or other key-value map; try to access a member.
      target = remaining_args[0]

      # Treat namedtuples as dicts when handling them as a map.
      if inspectutils.IsNamedTuple(component):
        component_dict = component._asdict()  # pytype: disable=attribute-error
      else:
        component_dict = component

      if target in component_dict:
        component = component_dict[target]
        handled = True
      elif target.replace('-', '_') in component_dict:
        component = component_dict[target.replace('-', '_')]
        handled = True
      else:
        for key, value in component_dict.items():
          if target == str(key):
            component = value
            handled = True
            break

      if handled:
        remaining_args = remaining_args[1:]
        filename = None
        lineno = None
        component_trace.AddAccessedProperty(
            component, target, [target], filename, lineno)
      else:
        error = FzError('Cannot find key:', target)
        candidate_errors.append((error, initial_args))

    if not handled and remaining_args:
      # Object handler. We'll try to access a member of the component.
      try:
        target = remaining_args[0]

        component, consumed_args, remaining_args = _GetMember(
            component, remaining_args)
        handled = True

        filename, lineno = inspectutils.GetFileAndLine(component)

        component_trace.AddAccessedProperty(
            component, target, consumed_args, filename, lineno)

      except FzError as error:
        # Couldn't access member.
        candidate_errors.append((error, initial_args))

    if not handled and is_callable_object:
      # The component is a callable object; we'll try to call it.
      try:
        component, remaining_args = _CallAndUpdateTrace(
            component,
            remaining_args,
            component_trace,
            treatment='callable')
        handled = True
      except FzError as error:
        candidate_errors.append((error, initial_args))

    if not handled and candidate_errors:
      error, initial_args = candidate_errors[0]
      component_trace.AddError(error, initial_args)
      return component_trace

    if used_separator:
      # Add back in the arguments from after the separator.
      if remaining_args:
        remaining_args = remaining_args + [separator] + saved_args
      elif (inspect.isclass(last_component)
            or inspect.isroutine(last_component)):
        remaining_args = saved_args
        component_trace.AddSeparator()
      elif component is not last_component:
        remaining_args = [separator] + saved_args
      else:
        # It was an unnecessary separator.
        remaining_args = saved_args

    if component is last_component and remaining_args == initial_args:
      # We're making no progress.
      break

  if remaining_args:
    component_trace.AddError(
        FzError('Could not consume arguments:', remaining_args),
        initial_args)
    return component_trace


  return component_trace




def _GetMember(component, args):

  members = dir(component)
  arg = args[0]
  arg_names = [
      arg,
      arg.replace('-', '_'),  # treat '-' as '_'.
  ]

  for arg_name in arg_names:
    if arg_name in members:
      return getattr(component, arg_name), [arg], args[1:]

  raise FzError('Could not consume arg:', arg)


def _CallAndUpdateTrace(component, args, component_trace, treatment='class',
                        target=None):
  if not target:
    target = component
  filename, lineno = inspectutils.GetFileAndLine(component)
  metadata = decorators.GetMetadata(component)
  fn = component.__call__ if treatment == 'callable' else component
  parse = _MakeParseFn(fn, metadata)
  (varargs, kwargs), consumed_args, remaining_args, capacity = parse(args)
  component = fn(*varargs, **kwargs)

  if treatment == 'class':
    action = trace.INSTANTIATED_CLASS
  elif treatment == 'routine':
    action = trace.CALLED_ROUTINE
  else:
    action = trace.CALLED_CALLABLE
  component_trace.AddCalledComponent(
      component, target, consumed_args, filename, lineno, capacity,
      action=action)

  return component, remaining_args


def _MakeParseFn(fn, metadata):

  fn_spec = inspectutils.GetFullArgSpec(fn)

  # Note: num_required_args is the number of positional arguments without
  # default values. All of these arguments are required.
  num_required_args = len(fn_spec.args) - len(fn_spec.defaults)
  required_kwonly = set(fn_spec.kwonlyargs) - set(fn_spec.kwonlydefaults)

  def _ParseFn(args):
    """Parses the list of `args` into (varargs, kwargs), remaining_args."""
    kwargs, remaining_kwargs, remaining_args = _ParseKeywordArgs(args, fn_spec)

    # Note: _ParseArgs modifies kwargs.
    parsed_args, kwargs, remaining_args, capacity = _ParseArgs(
        fn_spec.args, fn_spec.defaults, num_required_args, kwargs,
        remaining_args, metadata)

    if fn_spec.varargs or fn_spec.varkw:
      # If we're allowed *varargs or **kwargs, there's always capacity.
      capacity = True

    extra_kw = set(kwargs) - set(fn_spec.kwonlyargs)
    if fn_spec.varkw is None and extra_kw:
      raise FzError('Unexpected kwargs present:', extra_kw)

    missing_kwonly = set(required_kwonly) - set(kwargs)
    if missing_kwonly:
      raise FzError('Missing required flags:', missing_kwonly)

    # If we accept *varargs, then use all remaining arguments for *varargs.
    if fn_spec.varargs is not None:
      varargs, remaining_args = remaining_args, []
    else:
      varargs = []

    for index, value in enumerate(varargs):
      varargs[index] = _ParseValue(value, None, None, metadata)

    varargs = parsed_args + varargs
    remaining_args += remaining_kwargs

    consumed_args = args[:len(args) - len(remaining_args)]
    return (varargs, kwargs), consumed_args, remaining_args, capacity

  return _ParseFn


def _ParseArgs(fn_args, fn_defaults, num_required_args, kwargs,
               remaining_args, metadata):

  accepts_positional_args = metadata.get(decorators.ACCEPTS_POSITIONAL_ARGS)
  capacity = False  # If we see a default get used, we'll set capacity to True

  # Select unnamed args.
  parsed_args = []
  for index, arg in enumerate(fn_args):
    value = kwargs.pop(arg, None)
    if value is not None:  # A value is specified at the command line.
      value = _ParseValue(value, index, arg, metadata)
      parsed_args.append(value)
    else:  # No value has been explicitly specified.
      if remaining_args and accepts_positional_args:
        # Use a positional arg.
        value = remaining_args.pop(0)
        value = _ParseValue(value, index, arg, metadata)
        parsed_args.append(value)
      elif index < num_required_args:
        raise FzError(
            'The function received no value for the required argument:', arg)
      else:
        # We're past the args for which there's no default value.
        # There's a default value for this arg.
        capacity = True
        default_index = index - num_required_args  # index into the defaults.
        parsed_args.append(fn_defaults[default_index])

  for key, value in kwargs.items():
    kwargs[key] = _ParseValue(value, None, key, metadata)

  return parsed_args, kwargs, remaining_args, capacity


def _ParseKeywordArgs(args, fn_spec):

  kwargs = {}
  remaining_kwargs = []
  remaining_args = []
  fn_keywords = fn_spec.varkw
  fn_args = fn_spec.args + fn_spec.kwonlyargs

  if not args:
    return kwargs, remaining_kwargs, remaining_args

  skip_argument = False

  for index, argument in enumerate(args):
    if skip_argument:
      skip_argument = False
      continue

    if _IsFlag(argument):
      contains_equals = '=' in argument
      stripped_argument = argument.lstrip('-')
      if contains_equals:
        key, value = stripped_argument.split('=', 1)
      else:
        key = stripped_argument

      key = key.replace('-', '_')
      is_bool_syntax = (not contains_equals and
                        (index + 1 == len(args) or _IsFlag(args[index + 1])))

      # Determine the keyword.
      keyword = ''  # Indicates no valid keyword has been found yet.
      if (key in fn_args
          or (is_bool_syntax and key.startswith('no') and key[2:] in fn_args)
          or fn_keywords):
        keyword = key
      elif len(key) == 1:
        # This may be a shortcut flag.
        matching_fn_args = [arg for arg in fn_args if arg[0] == key]
        if len(matching_fn_args) == 1:
          keyword = matching_fn_args[0]
        elif len(matching_fn_args) > 1:
          raise FzError("The argument '{}' is ambiguous as it could "
                          "refer to any of the following arguments: {}".format(
                              argument, matching_fn_args))

      # Determine the value.
      if not keyword:
        got_argument = False
      elif contains_equals:
        # Already got the value above.
        got_argument = True
      elif is_bool_syntax:
        # There's no next arg or the next arg is a Flag, so we consider this
        # flag to be a boolean.
        got_argument = True
        if keyword in fn_args:
          value = 'True'
        elif keyword.startswith('no'):
          keyword = keyword[2:]
          value = 'False'
        else:
          value = 'True'
      else:
        # The assert should pass. Otherwise either contains_equals or
        # is_bool_syntax would have been True.
        assert index + 1 < len(args)
        value = args[index + 1]
        got_argument = True

      # In order for us to consume the argument as a keyword arg, we either:
      # Need to be explicitly expecting the keyword, or we need to be
      # accepting **kwargs.
      skip_argument = not contains_equals and not is_bool_syntax
      if got_argument:
        kwargs[keyword] = value
      else:
        remaining_kwargs.append(argument)
        if skip_argument:
          remaining_kwargs.append(args[index + 1])
    else:  # not _IsFlag(argument)
      remaining_args.append(argument)

  return kwargs, remaining_kwargs, remaining_args


def _IsFlag(argument):

  return _IsSingleCharFlag(argument) or _IsMultiCharFlag(argument)


def _IsSingleCharFlag(argument):
  """Determines if the argument is a single char flag (e.g. '-a')."""
  return re.match('^-[a-zA-Z]$', argument) or re.match('^-[a-zA-Z]=', argument)


def _IsMultiCharFlag(argument):
  """Determines if the argument is a multi char flag (e.g. '--alpha')."""
  return argument.startswith('--') or re.match('^-[a-zA-Z]', argument)


def _ParseValue(value, index, arg, metadata):

  parse_fn = parser.DefaultParseValue

  # We check to see if any parse function from the fn metadata applies here.
  parse_fns = metadata.get(decorators.FZ_PARSE_FNS)
  if parse_fns:
    default = parse_fns['default']
    positional = parse_fns['positional']
    named = parse_fns['named']

    if index is not None and 0 <= index < len(positional):
      parse_fn = positional[index]
    elif arg in named:
      parse_fn = named[arg]
    elif default is not None:
      parse_fn = default

  return parse_fn(value)
