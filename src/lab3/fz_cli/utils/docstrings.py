

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import collections
import re
import textwrap

import enum


class DocstringInfo(
    collections.namedtuple(
        'DocstringInfo',
        ('summary', 'description', 'args', 'returns', 'yields', 'raises'))):
  pass
DocstringInfo.__new__.__defaults__ = (None,) * len(DocstringInfo._fields)


class ArgInfo(
    collections.namedtuple(
        'ArgInfo',
        ('name', 'type', 'description'))):
  pass
ArgInfo.__new__.__defaults__ = (None,) * len(ArgInfo._fields)


class Namespace(dict):

  def __getattr__(self, key):
    if key not in self:
      self[key] = Namespace()
    return self[key]

  def __setattr__(self, key, value):
    self[key] = value

  def __delattr__(self, key):
    if key in self:
      del self[key]


class Sections(enum.Enum):
  ARGS = 0
  RETURNS = 1
  YIELDS = 2
  RAISES = 3
  TYPE = 4


class Formats(enum.Enum):
  GOOGLE = 0
  NUMPY = 1
  RST = 2


SECTION_TITLES = {
    Sections.ARGS: ('argument', 'arg', 'parameter', 'param'),
    Sections.RETURNS: ('return',),
    Sections.YIELDS: ('yield',),
    Sections.RAISES: ('raise', 'except', 'exception', 'throw', 'error', 'warn'),
    Sections.TYPE: ('type',),  # rst-only
}


def parse(docstring):
  if docstring is None:
    return DocstringInfo()

  lines = docstring.strip().split('\n')
  lines_len = len(lines)
  state = Namespace()  # TODO(dbieber): Switch to an explicit class.

  # Variables in state include:
  state.section.title = None
  state.section.indentation = None
  state.section.line1_indentation = None
  state.section.format = None
  state.summary.permitted = True
  state.summary.lines = []
  state.description.lines = []
  state.args = []
  state.current_arg = None
  state.returns.lines = []
  state.yields.lines = []
  state.raises.lines = []

  for index, line in enumerate(lines):
    has_next = index + 1 < lines_len
    previous_line = lines[index - 1] if index > 0 else None
    next_line = lines[index + 1] if has_next else None
    line_info = _create_line_info(line, next_line, previous_line)
    _consume_line(line_info, state)

  summary = ' '.join(state.summary.lines) if state.summary.lines else None
  state.description.lines = _strip_blank_lines(state.description.lines)
  description = textwrap.dedent('\n'.join(state.description.lines))
  if not description:
    description = None
  returns = _join_lines(state.returns.lines)
  yields = _join_lines(state.yields.lines)
  raises = _join_lines(state.raises.lines)

  args = [ArgInfo(
      name=arg.name, type=_cast_to_known_type(_join_lines(arg.type.lines)),
      description=_join_lines(arg.description.lines)) for arg in state.args]

  return DocstringInfo(
      summary=summary,
      description=description,
      args=args or None,
      returns=returns,
      raises=raises,
      yields=yields,
  )


def _strip_blank_lines(lines):
  start = 0
  num_lines = len(lines)
  while lines and start < num_lines and _is_blank(lines[start]):
    start += 1

  lines = lines[start:]

  # Remove trailing blank lines.
  while lines and _is_blank(lines[-1]):
    lines.pop()

  return lines


def _is_blank(line):
  return not line or line.isspace()


def _join_lines(lines):
  if not lines:
    return None

  started = False
  group_texts = []  # Full text of each section.
  group_lines = []  # Lines within the current section.
  for line in lines:
    stripped_line = line.strip()
    if stripped_line:
      started = True
      group_lines.append(stripped_line)
    else:
      if started:
        group_text = ' '.join(group_lines)
        group_texts.append(group_text)
        group_lines = []

  if group_lines:  # Process the final group.
    group_text = ' '.join(group_lines)
    group_texts.append(group_text)

  return '\n\n'.join(group_texts)


def _get_or_create_arg_by_name(state, name):
  for arg in state.args:
    if arg.name == name:
      return arg
  arg = Namespace()
  arg.name = name
  arg.type.lines = []
  arg.description.lines = []
  state.args.append(arg)
  return arg


def _is_arg_name(name):
  name = name.strip()
  return (name
          and ' ' not in name
          and ':' not in name)


def _as_arg_name_and_type(text):
  tokens = text.split()
  if len(tokens) < 2:
    return None
  if _is_arg_name(tokens[0]):
    type_token = ' '.join(tokens[1:])
    type_token = type_token.lstrip('{([').rstrip('])}')
    return tokens[0], type_token
  else:
    return None


def _as_arg_names(names_str):
  names = re.split(',| ', names_str)
  names = [name.strip() for name in names if name.strip()]
  for name in names:
    if not _is_arg_name(name):
      return None
  if not names:
    return None
  return names


def _cast_to_known_type(name):
  if name is None:
    return None
  return name.rstrip('.')


def _consume_google_args_line(line_info, state):
  """Consume a single line from a Google args section."""
  split_line = line_info.remaining.split(':', 1)
  if len(split_line) > 1:
    first, second = split_line  # first is either the "arg" or "arg (type)"
    if _is_arg_name(first.strip()):
      arg = _get_or_create_arg_by_name(state, first.strip())
      arg.description.lines.append(second.strip())
      state.current_arg = arg
    else:
      arg_name_and_type = _as_arg_name_and_type(first)
      if arg_name_and_type:
        arg_name, type_str = arg_name_and_type
        arg = _get_or_create_arg_by_name(state, arg_name)
        arg.type.lines.append(type_str)
        arg.description.lines.append(second.strip())
      else:
        if state.current_arg:
          state.current_arg.description.lines.append(split_line[0])
  else:
    if state.current_arg:
      state.current_arg.description.lines.append(split_line[0])


def _consume_line(line_info, state):
  _update_section_state(line_info, state)

  if state.section.title is None:
    if state.summary.permitted:
      if line_info.remaining:
        state.summary.lines.append(line_info.remaining)
      elif state.summary.lines:
        state.summary.permitted = False
    else:
      state.description.lines.append(line_info.remaining_raw)
  else:
    state.summary.permitted = False

  if state.section.new and state.section.format == Formats.RST:
    # The current line starts with an RST directive, e.g. ":param arg:".
    directive = _get_directive(line_info)
    directive_tokens = directive.split()  # pytype: disable=attribute-error
    if state.section.title == Sections.ARGS:
      name = directive_tokens[-1]
      arg = _get_or_create_arg_by_name(state, name)
      if len(directive_tokens) == 3:
        # A param directive of the form ":param type arg:".
        arg.type.lines.append(directive_tokens[1])
      state.current_arg = arg
    elif state.section.title == Sections.TYPE:
      name = directive_tokens[-1]
      arg = _get_or_create_arg_by_name(state, name)
      state.current_arg = arg

  if (state.section.format == Formats.NUMPY and
      _line_is_hyphens(line_info.remaining)):
    # Skip this all-hyphens line, which is part of the numpy section header.
    return

  if state.section.title == Sections.ARGS:
    if state.section.format == Formats.GOOGLE:
      _consume_google_args_line(line_info, state)
    elif state.section.format == Formats.RST:
      state.current_arg.description.lines.append(line_info.remaining.strip())
    elif state.section.format == Formats.NUMPY:
      line_stripped = line_info.remaining.strip()
      if _is_arg_name(line_stripped):
        arg = _get_or_create_arg_by_name(state, line_stripped)
        state.current_arg = arg
      elif _line_is_numpy_parameter_type(line_info):
        possible_args, type_data = line_stripped.split(':', 1)
        arg_names = _as_arg_names(possible_args)  # re.split(' |,', s)
        if arg_names:
          for arg_name in arg_names:
            arg = _get_or_create_arg_by_name(state, arg_name)
            arg.type.lines.append(type_data)
            state.current_arg = arg
        else:  # Just an ordinary line.
          if state.current_arg:
            state.current_arg.description.lines.append(
                line_info.remaining.strip())
          else:
            pass
      else:  # Just an ordinary line.
        if state.current_arg:
          state.current_arg.description.lines.append(
              line_info.remaining.strip())
        else:
          pass

  elif state.section.title == Sections.RETURNS:
    state.returns.lines.append(line_info.remaining.strip())
  elif state.section.title == Sections.YIELDS:
    state.yields.lines.append(line_info.remaining.strip())
  elif state.section.title == Sections.RAISES:
    state.raises.lines.append(line_info.remaining.strip())
  elif state.section.title == Sections.TYPE:
    if state.section.format == Formats.RST:
      assert state.current_arg is not None
      state.current_arg.type.lines.append(line_info.remaining.strip())
    else:
      pass


def _create_line_info(line, next_line, previous_line):
  line_info = Namespace()
  line_info.line = line
  line_info.stripped = line.strip()
  line_info.remaining_raw = line_info.line
  line_info.remaining = line_info.stripped
  line_info.indentation = len(line) - len(line.lstrip())
  line_info.next.line = next_line
  next_line_exists = next_line is not None
  line_info.next.stripped = next_line.strip() if next_line_exists else None
  line_info.next.indentation = (
      len(next_line) - len(next_line.lstrip()) if next_line_exists else None)
  line_info.previous.line = previous_line
  previous_line_exists = previous_line is not None
  line_info.previous.indentation = (
      len(previous_line) -
      len(previous_line.lstrip()) if previous_line_exists else None)
  return line_info


def _update_section_state(line_info, state):
  section_updated = False

  google_section_permitted = _google_section_permitted(line_info, state)
  google_section = google_section_permitted and _google_section(line_info)
  if google_section:
    state.section.format = Formats.GOOGLE
    state.section.title = google_section
    line_info.remaining = _get_after_google_header(line_info)
    line_info.remaining_raw = line_info.remaining
    section_updated = True

  rst_section = _rst_section(line_info)
  if rst_section:
    state.section.format = Formats.RST
    state.section.title = rst_section
    line_info.remaining = _get_after_directive(line_info)
    line_info.remaining_raw = line_info.remaining
    section_updated = True

  numpy_section = _numpy_section(line_info)
  if numpy_section:
    state.section.format = Formats.NUMPY
    state.section.title = numpy_section
    line_info.remaining = ''
    line_info.remaining_raw = line_info.remaining
    section_updated = True

  if section_updated:
    state.section.new = True
    state.section.indentation = line_info.indentation
    state.section.line1_indentation = line_info.next.indentation
  else:
    state.section.new = False


def _google_section_permitted(line_info, state):
  if state.section.indentation is None:  # We're not in a section yet.
    return True
  return (line_info.indentation <= state.section.indentation
          or line_info.indentation < state.section.line1_indentation)


def _matches_section_title(title, section_title):
  title = title.lower()
  section_title = section_title.lower()
  return section_title in (title, title[:-1])  # Supports plurals / some typos.


def _matches_section(title, section):
  for section_title in SECTION_TITLES[section]:
    if _matches_section_title(title, section_title):
      return True
  return False


def _section_from_possible_title(possible_title):
  for section in SECTION_TITLES:
    if _matches_section(possible_title, section):
      return section
  return None


def _google_section(line_info):
  colon_index = line_info.remaining.find(':')
  possible_title = line_info.remaining[:colon_index]
  return _section_from_possible_title(possible_title)


def _get_after_google_header(line_info):
  """Gets the remainder of the line, after a Google header."""
  colon_index = line_info.remaining.find(':')
  return line_info.remaining[colon_index + 1:]


def _get_directive(line_info):
  if line_info.stripped.startswith(':'):
    return line_info.stripped.split(':', 2)[1]
  else:
    return None


def _get_after_directive(line_info):
  sections = line_info.stripped.split(':', 2)
  if len(sections) > 2:
    return sections[-1]
  else:
    return ''


def _rst_section(line_info):
  directive = _get_directive(line_info)
  if directive:
    possible_title = directive.split()[0]
    return _section_from_possible_title(possible_title)
  else:
    return None


def _line_is_hyphens(line):
  return line and not line.strip('-')


def _numpy_section(line_info):
  next_line_is_hyphens = _line_is_hyphens(line_info.next.stripped)
  if next_line_is_hyphens:
    possible_title = line_info.remaining
    return _section_from_possible_title(possible_title)
  else:
    return None


def _line_is_numpy_parameter_type(line_info):
  line_stripped = line_info.remaining.strip()
  if ':' in line_stripped:
    previous_indent = line_info.previous.indentation
    current_indent = line_info.indentation
    if ':' in line_info.previous.line and current_indent > previous_indent:
      # The parameter type was the previous line; this is the description.
      return False
    else:
      return True
  return False
