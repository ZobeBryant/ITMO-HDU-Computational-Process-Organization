from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect

FZ_METADATA = 'FZ_METADATA'
FZ_PARSE_FNS = 'FZ_PARSE_FNS'
ACCEPTS_POSITIONAL_ARGS = 'ACCEPTS_POSITIONAL_ARGS'


def SetParseFn(fn, *arguments):

  def _Decorator(func):
    parse_fns = GetParseFns(func)
    if not arguments:
      parse_fns['default'] = fn
    else:
      for argument in arguments:
        parse_fns['named'][argument] = fn
    _SetMetadata(func, FZ_PARSE_FNS, parse_fns)
    return func

  return _Decorator


def SetParseFns(*positional, **named):

  def _Decorator(fn):
    parse_fns = GetParseFns(fn)
    parse_fns['positional'] = positional
    parse_fns['named'].update(named)
    _SetMetadata(fn, FZ_PARSE_FNS, parse_fns)
    return fn

  return _Decorator


def _SetMetadata(fn, attribute, value):
  metadata = GetMetadata(fn)
  metadata[attribute] = value
  setattr(fn, FZ_METADATA, metadata)


def GetMetadata(fn):
  default = {
      ACCEPTS_POSITIONAL_ARGS: inspect.isroutine(fn),
  }
  return getattr(fn, FZ_METADATA, default)


def GetParseFns(fn):
  metadata = GetMetadata(fn)
  default = dict(default=None, positional=[], named={})
  return metadata.get(FZ_PARSE_FNS, default)
