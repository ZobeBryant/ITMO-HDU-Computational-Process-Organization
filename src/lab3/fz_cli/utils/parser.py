
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import ast


def CreateParser():
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('--verbose', '-v', action='store_true')
  parser.add_argument('--separator', default='-')
  parser.add_argument('--help', '-h', action='store_true')
  parser.add_argument('--trace', '-t', action='store_true')
  return parser


def SeparateFlagArgs(args):
  if '--' in args:
    separator_index = len(args) - 1 - args[::-1].index('--')  # index of last --
    flag_args = args[separator_index + 1:]
    args = args[:separator_index]
    return args, flag_args
  return args, []


def DefaultParseValue(value):
  try:
    return _LiteralEval(value)
  except (SyntaxError, ValueError):
    # If _LiteralEval can't parse the value, treat it as a string.
    return value


def _LiteralEval(value):
  root = ast.parse(value, mode='eval')
  if isinstance(root.body, ast.BinOp):  # pytype: disable=attribute-error
    raise ValueError(value)

  for node in ast.walk(root):
    for field, child in ast.iter_fields(node):
      if isinstance(child, list):
        for index, subchild in enumerate(child):
          if isinstance(subchild, ast.Name):
            child[index] = _Replacement(subchild)

      elif isinstance(child, ast.Name):
        replacement = _Replacement(child)
        node.__setattr__(field, replacement)

  return ast.literal_eval(root)


def _Replacement(node):
  value = node.id
  # These are the only builtin constants supported by literal_eval.
  if value in ('True', 'False', 'None'):
    return node
  return ast.Str(value)
