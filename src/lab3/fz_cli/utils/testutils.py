
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import re
import sys
import unittest

from fz_cli import cli_core as core
from fz_cli import trace

import mock
import six


class BaseTestCase(unittest.TestCase):
  """Shared test case for Python Fz tests."""

  @contextlib.contextmanager
  def assertOutputMatches(self, stdout='.*', stderr='.*', capture=True):

    stdout_fp = six.StringIO()
    stderr_fp = six.StringIO()
    try:
      with mock.patch.object(sys, 'stdout', stdout_fp):
        with mock.patch.object(sys, 'stderr', stderr_fp):
          yield
    finally:
      if not capture:
        sys.stdout.write(stdout_fp.getvalue())
        sys.stderr.write(stderr_fp.getvalue())

    for name, regexp, fp in [('stdout', stdout, stdout_fp),
                             ('stderr', stderr, stderr_fp)]:
      value = fp.getvalue()
      if regexp is None:
        if value:
          raise AssertionError('%s: Expected no output. Got: %r' %
                               (name, value))
      else:
        if not re.search(regexp, value, re.DOTALL | re.MULTILINE):
          raise AssertionError('%s: Expected %r to match %r' %
                               (name, value, regexp))

  @contextlib.contextmanager
  def assertRaisesFzExit(self, code, regexp='.*'):

    with self.assertOutputMatches(stderr=regexp):
      with self.assertRaises(core.FzExit):
        try:
          yield
        except core.FzExit as exc:
          if exc.code != code:
            raise AssertionError('Incorrect exit code: %r != %r' % (exc.code,
                                                                    code))
          self.assertIsInstance(exc.trace, trace.FzTrace)
          raise



main = unittest.main
skip = unittest.skip
skipIf = unittest.skipIf

