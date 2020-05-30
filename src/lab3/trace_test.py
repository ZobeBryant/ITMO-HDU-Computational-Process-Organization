
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from fz_cli.utils import testutils
from fz_cli import trace


class FzTraceTest(testutils.BaseTestCase):

  def testFzTraceInitialization(self):
    t = trace.FzTrace(10)
    self.assertIsNotNone(t)
    self.assertIsNotNone(t.elements)

  def testFzTraceGetResult(self):
    t = trace.FzTrace('start')
    self.assertEqual(t.GetResult(), 'start')
    t.AddAccessedProperty('t', 'final', None, 'example.py', 10)
    self.assertEqual(t.GetResult(), 't')

  def testFzTraceHasError(self):
    t = trace.FzTrace('start')
    self.assertFalse(t.HasError())
    t.AddAccessedProperty('t', 'final', None, 'example.py', 10)
    self.assertFalse(t.HasError())
    t.AddError(ValueError('example error'), ['arg'])
    self.assertTrue(t.HasError())

  def testAddAccessedProperty(self):
    t = trace.FzTrace('initial object')
    args = ('example', 'args')
    t.AddAccessedProperty('new component', 'prop', args, 'sample.py', 12)
    self.assertEqual(
        str(t),
        '1. Initial component\n2. Accessed property "prop" (sample.py:12)')

  def testAddCalledCallable(self):
    t = trace.FzTrace('initial object')
    args = ('example', 'args')
    t.AddCalledComponent('result', 'cell', args, 'sample.py', 10, False,
                         action=trace.CALLED_CALLABLE)
    self.assertEqual(
        str(t),
        '1. Initial component\n2. Called callable "cell" (sample.py:10)')

  def testAddCalledRoutine(self):
    t = trace.FzTrace('initial object')
    args = ('example', 'args')
    t.AddCalledComponent('result', 'run', args, 'sample.py', 12, False,
                         action=trace.CALLED_ROUTINE)
    self.assertEqual(
        str(t),
        '1. Initial component\n2. Called routine "run" (sample.py:12)')

  def testAddInstantiatedClass(self):
    t = trace.FzTrace('initial object')
    args = ('example', 'args')
    t.AddCalledComponent(
        'Classname', 'classname', args, 'sample.py', 12, False,
        action=trace.INSTANTIATED_CLASS)
    target = """1. Initial component
2. Instantiated class "classname" (sample.py:12)"""
    self.assertEqual(str(t), target)


  def testGetCommand(self):
    t = trace.FzTrace('initial object')
    args = ('example', 'args')
    t.AddCalledComponent('result', 'run', args, 'sample.py', 12, False,
                         action=trace.CALLED_ROUTINE)
    self.assertEqual(t.GetCommand(), 'example args')

  def testGetCommandWithQuotes(self):
    t = trace.FzTrace('initial object')
    args = ('example', 'spaced arg')
    t.AddCalledComponent('result', 'run', args, 'sample.py', 12, False,
                         action=trace.CALLED_ROUTINE)
    self.assertEqual(t.GetCommand(), "example 'spaced arg'")

  def testGetCommandWithFlagQuotes(self):
    t = trace.FzTrace('initial object')
    args = ('--example=spaced arg',)
    t.AddCalledComponent('result', 'run', args, 'sample.py', 12, False,
                         action=trace.CALLED_ROUTINE)
    self.assertEqual(t.GetCommand(), "--example='spaced arg'")


class FzTraceElementTest(testutils.BaseTestCase):

  def testFzTraceElementHasError(self):
    el = trace.FzTraceElement()
    self.assertFalse(el.HasError())

    el = trace.FzTraceElement(error=ValueError('example error'))
    self.assertTrue(el.HasError())

  def testFzTraceElementAsStringNoMetadata(self):
    el = trace.FzTraceElement(
        component='Example',
        action='Fake action',
    )
    self.assertEqual(str(el), 'Fake action')

  def testFzTraceElementAsStringWithTarget(self):
    el = trace.FzTraceElement(
        component='Example',
        action='Created toy',
        target='Beaker',
    )
    self.assertEqual(str(el), 'Created toy "Beaker"')

  def testFzTraceElementAsStringWithTargetAndLineNo(self):
    el = trace.FzTraceElement(
        component='Example',
        action='Created toy',
        target='Beaker',
        filename='beaker.py',
        lineno=10,
    )
    self.assertEqual(str(el), 'Created toy "Beaker" (beaker.py:10)')


if __name__ == '__main__':
  testutils.main()
