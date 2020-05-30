from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import fz_cli
from fz_cli.utils import testutils, test_components as tc
import mock


class FzTest(testutils.BaseTestCase):

  def testFz(self):
    with mock.patch.object(sys, 'argv', ['progname']):
      fz_cli.Fz(tc.Empty)
      fz_cli.Fz(tc.OldStyleEmpty)
      fz_cli.Fz(tc.WithInit)
    # Test both passing command as a sequence and as a string.
    self.assertEqual(fz_cli.Fz(tc.NoDefaults, command='triple 4'), 12)
    self.assertEqual(fz_cli.Fz(tc.WithDefaults, command=('double', '2')), 4)
    self.assertEqual(fz_cli.Fz(tc.WithDefaults, command=['triple', '4']), 12)
    self.assertEqual(fz_cli.Fz(tc.OldStyleWithDefaults,
                               command=['double', '2']), 4)
    self.assertEqual(fz_cli.Fz(tc.OldStyleWithDefaults,
                               command=['triple', '4']), 12)

  def testFzPositionalCommand(self):
    # Test passing command as a positional argument.
    self.assertEqual(fz_cli.Fz(tc.NoDefaults, 'double 2'), 4)
    self.assertEqual(fz_cli.Fz(tc.NoDefaults, ['double', '2']), 4)

  def testFzInvalidCommandArg(self):
    with self.assertRaises(ValueError):
      # This is not a valid command.
      fz_cli.Fz(tc.WithDefaults, command=10)

  def testFzNoArgs(self):
    self.assertEqual(fz_cli.Fz(tc.MixedDefaults, command=['ten']), 10)

  def testFzExceptions(self):
    # Exceptions of Fz are printed to stderr and a FzExit is raised.
    with self.assertRaisesFzExit(2):
      fz_cli.Fz(tc.Empty, command=['nomethod'])  # Member doesn't exist.
    with self.assertRaisesFzExit(2):
      fz_cli.Fz(tc.NoDefaults, command=['double'])  # Missing argument.
    with self.assertRaisesFzExit(2):
      fz_cli.Fz(tc.TypedProperties, command=['delta', 'x'])  # Missing key.

    # Exceptions of the target components are still raised.
    with self.assertRaises(ZeroDivisionError):
      fz_cli.Fz(tc.NumberDefaults, command=['reciprocal', '0.0'])

  def testFzNamedArgs(self):
    self.assertEqual(fz_cli.Fz(tc.WithDefaults,
                               command=['double', '--count', '5']), 10)
    self.assertEqual(fz_cli.Fz(tc.WithDefaults,
                               command=['triple', '--count', '5']), 15)
    self.assertEqual(
        fz_cli.Fz(tc.OldStyleWithDefaults, command=['double', '--count', '5']),
        10)
    self.assertEqual(
        fz_cli.Fz(tc.OldStyleWithDefaults, command=['triple', '--count', '5']),
        15)

  def testFzNamedArgsSingleHyphen(self):
    self.assertEqual(fz_cli.Fz(tc.WithDefaults,
                               command=['double', '-count', '5']), 10)
    self.assertEqual(fz_cli.Fz(tc.WithDefaults,
                               command=['triple', '-count', '5']), 15)
    self.assertEqual(
        fz_cli.Fz(tc.OldStyleWithDefaults, command=['double', '-count', '5']),
        10)
    self.assertEqual(
        fz_cli.Fz(tc.OldStyleWithDefaults, command=['triple', '-count', '5']),
        15)



if __name__ == '__main__':
  testutils.main()
