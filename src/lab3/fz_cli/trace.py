

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pipes

from fz_cli.utils import inspectutils

INITIAL_COMPONENT = 'Initial component'
INSTANTIATED_CLASS = 'Instantiated class'
CALLED_ROUTINE = 'Called routine'
CALLED_CALLABLE = 'Called callable'
ACCESSED_PROPERTY = 'Accessed property'



class FzTrace(object):
  """A FzTrace represents the steps taken during a single Fz execution.

  A FzTrace consists of a sequence of FzTraceElement objects. Each element
  represents an action taken by Fz during a single Fz execution. An action
  may be instantiating a class, calling a routine, or accessing a property.
  """

  def __init__(self, initial_component, name=None, separator='-', verbose=False,
               show_help=False, show_trace=False):
    initial_trace_element = FzTraceElement(
        component=initial_component,
        action=INITIAL_COMPONENT,
    )

    self.name = name
    self.separator = separator
    self.elements = [initial_trace_element]
    self.verbose = verbose
    self.show_help = show_help
    self.show_trace = show_trace

  def GetResult(self):
    """Returns the component from the last element of the trace."""
    return self.GetLastHealthyElement().component


  def GetLastHealthyElement(self):
    """Returns the last element of the trace that is not an error.

    This element will contain the final component indicated by the trace.

    Returns:
      The last element of the trace that is not an error.
    """
    for element in reversed(self.elements):
      if not element.HasError():
        return element
    return None

  def HasError(self):
    """Returns whether the Fz execution encountered a Fz usage error."""
    return self.elements[-1].HasError()

  def AddAccessedProperty(self, component, target, args, filename, lineno):
    element = FzTraceElement(
        component=component,
        action=ACCESSED_PROPERTY,
        target=target,
        args=args,
        filename=filename,
        lineno=lineno,
    )
    self.elements.append(element)

  def AddCalledComponent(self, component, target, args, filename, lineno,
                         capacity, action=CALLED_CALLABLE):
    """Adds an element to the trace indicating that a component was called.
    Also applies to instantiating a class.
    """
    element = FzTraceElement(
        component=component,
        action=action,
        target=target,
        args=args,
        filename=filename,
        lineno=lineno,
        capacity=capacity,
    )
    self.elements.append(element)



  def AddError(self, error, args):
    element = FzTraceElement(error=error, args=args)
    self.elements.append(element)

  def AddSeparator(self):

    self.elements[-1].AddSeparator()

  def _Quote(self, arg):
    if arg.startswith('--') and '=' in arg:
      prefix, value = arg.split('=', 1)
      return pipes.quote(prefix) + '=' + pipes.quote(value)
    return pipes.quote(arg)

  def GetCommand(self, include_separators=True):
    """Returns the command representing the trace up to this point.

    Args:
      include_separators: Whether or not to include separators in the command.

    Returns:
      A string representing a Fz CLI command that would produce this trace.
    """
    args = []
    if self.name:
      args.append(self.name)

    for element in self.elements:
      if element.HasError():
        continue
      if element.args:
        args.extend(element.args)
      if element.HasSeparator() and include_separators:
        args.append(self.separator)

    if self.NeedsSeparator() and include_separators:
      args.append(self.separator)

    return ' '.join(self._Quote(arg) for arg in args)

  def NeedsSeparator(self):
    """Returns whether a separator should be added to the command.
    """
    element = self.GetLastHealthyElement()
    return element.HasCapacity() and not element.HasSeparator()

  def __str__(self):
    lines = []
    for index, element in enumerate(self.elements):
      line = '{index}. {trace_string}'.format(
          index=index + 1,
          trace_string=element,
      )
      lines.append(line)
    return '\n'.join(lines)

  def NeedsSeparatingHyphenHyphen(self, flag='help'):
    """Returns whether a the trace need '--' before '--help'.

    '--' is needed when the component takes keyword arguments, when the value of
    flag matches one of the argument of the component, or the component takes in
    keyword-only arguments(e.g. argument with default value).

    Args:
      flag: the flag available for the trace

    Returns:
      True for needed '--', False otherwise.

    """
    element = self.GetLastHealthyElement()
    component = element.component
    spec = inspectutils.GetFullArgSpec(component)
    return (spec.varkw is not None
            or flag in spec.args
            or flag in spec.kwonlyargs)


class FzTraceElement(object):
  """A FzTraceElement represents a single step taken by a Fz execution.

  Examples of a FzTraceElement are the instantiation of a class or the
  accessing of an object member.
  """

  def __init__(self,
               component=None,
               action=None,
               target=None,
               args=None,
               filename=None,
               lineno=None,
               error=None,
               capacity=None):

    self.component = component
    self._action = action
    self._target = target
    self.args = args
    self._filename = filename
    self._lineno = lineno
    self._error = error
    self._separator = False
    self._capacity = capacity

  def HasError(self):
    return self._error is not None

  def HasCapacity(self):
    return self._capacity

  def HasSeparator(self):
    return self._separator

  def AddSeparator(self):
    self._separator = True

  def ErrorAsStr(self):
    return ' '.join(str(arg) for arg in self._error.args)

  def __str__(self):
    if self.HasError():
      return self.ErrorAsStr()
    else:
      # Format is: {action} "{target}" ({filename}:{lineno})
      string = self._action
      if self._target is not None:
        string += ' "{target}"'.format(target=self._target)
      if self._filename is not None:
        path = self._filename
        if self._lineno is not None:
          path += ':{lineno}'.format(lineno=self._lineno)

        string += ' ({path})'.format(path=path)
      return string
