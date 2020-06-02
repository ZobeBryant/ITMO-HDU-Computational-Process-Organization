import unittest
from StateMachine import *

class FiniteStateMachineTest(unittest.TestCase):
    def test_state_machine(self):
        fsm = FiniteStateMachine("One Way Traffic Light")
        fsm.add_state("Green",{'Green':True, 'Yellow':False, 'Red':False})
        fsm.add_state("Yellow", {'Green': False, 'Yellow': True, 'Red': False})
        fsm.add_state("Red", {'Green': False, 'Yellow': False, 'Red': True})

        fsm.add_transition("Green2Yellow","Green","Yellow",lambda clk_n: clk_n >= 5, lambda clk_n: 1)
        fsm.add_transition("Keep Green", "Green", "Green", lambda clk_n: clk_n < 5, lambda clk_n: clk_n+1)
        fsm.add_transition("Yellow2Ted", "Yellow", "Red", lambda clk_n: clk_n >= 1, lambda clk_n: 1)
        fsm.add_transition("Keep Yellow", "Yellow", "Yellow", lambda clk_n: clk_n < 1,lambda clk_n: clk_n+1)
        fsm.add_transition("Red2Green", "Red", "Green", lambda clk_n: clk_n >= 6, lambda clk_n: 1)
        fsm.add_transition("Keep Red", "Red", "Red", lambda clk_n: clk_n < 6, lambda clk_n: clk_n+1)

        actual = fsm.execute("Green", total_clk=14, clk_n=0)
        expect = {'Green':True, 'Yellow':False, 'Red':False}
        self.assertEqual(actual, expect)
        self.assertEqual(fsm.light_state_history,[
            (1, {'Green': True, 'Yellow': False, 'Red': False}),
            (2, {'Green': True, 'Yellow': False, 'Red': False}),
            (3, {'Green': True, 'Yellow': False, 'Red': False}),
            (4, {'Green': True, 'Yellow': False, 'Red': False}),
            (5, {'Green': True, 'Yellow': False, 'Red': False}),
            (6, {'Green': False, 'Yellow': True, 'Red': False}),
            (7, {'Green': False, 'Yellow': False, 'Red': True}),
            (8, {'Green': False, 'Yellow': False, 'Red': True}),
            (9, {'Green': False, 'Yellow': False, 'Red': True}),
            (10, {'Green': False, 'Yellow': False, 'Red': True}),
            (11, {'Green': False, 'Yellow': False, 'Red': True}),
            (12, {'Green': False, 'Yellow': False, 'Red': True}),
            (13, {'Green': True, 'Yellow': False, 'Red': False}),
            (14, {'Green': True, 'Yellow': False, 'Red': False})
        ])
        self.assertEqual(fsm.event_history,[
            (1, 'Keep Green', 1),
            (2, 'Keep Green', 2),
            (3, 'Keep Green', 3),
            (4, 'Keep Green', 4),
            (5, 'Keep Green', 5),
            (6, 'Green2Yellow', 1),
            (7, 'Yellow2Ted', 1),
            (8, 'Keep Red', 2),
            (9, 'Keep Red', 3),
            (10, 'Keep Red', 4),
            (11, 'Keep Red', 5),
            (12, 'Keep Red', 6),
            (13, 'Red2Green', 1),
            (14, 'Keep Green', 2)
        ])

    def test_crossroad_state_machine(self):
        fsm = FiniteStateMachine("Crossroad Traffic Light")
        fsm.add_state("N-S:Green,W-E:Red", {'N-S Green': True, 'N-S Yellow': False, 'N-S Red': False,
                                            'W-E Green': False, 'W-E Yellow': False, 'W-E Red':True})
        fsm.add_state("N-S:Yellow,W-E:Red", {'N-S Green': False, 'N-S Yellow': True, 'N-S Red': False,
                                            'W-E Green': False, 'W-E Yellow': False, 'W-E Red': True })
        fsm.add_state("N-S:Red,W-E:Green", {'N-S Green': False, 'N-S Yellow': False, 'N-S Red': True,
                                            'W-E Green': True, 'W-E Yellow': False, 'W-E Red': False, })
        fsm.add_state("N-S:Red,W-E:Yellow", {'N-S Green': False, 'N-S Yellow': False, 'N-S Red': True,
                                            'W-E Green': False, 'W-E Yellow': True, 'W-E Red': False })
        fsm.add_transition("N-S:Green2Yellow,W-E:Keep Red", "N-S:Green,W-E:Red", "N-S:Yellow,W-E:Red",
                           lambda clk_n: clk_n >= 5, lambda clk_n: 1)
        fsm.add_transition("N-S:Keep Green,W-E:Keep Red", "N-S:Green,W-E:Red", "N-S:Green,W-E:Red",
                           lambda clk_n: clk_n < 5, lambda clk_n: clk_n + 1)
        fsm.add_transition("N-S:Yellow2Red,W-E:Red2Green", "N-S:Yellow,W-E:Red", "N-S:Red,W-E:Green",
                           lambda clk_n: clk_n >= 1, lambda clk_n: 1)
        fsm.add_transition("N-S:KeepYellow,W-E:Keep Red", "N-S:Yellow,W-E:Red", "N-S:Yellow,W-E:Red",
                           lambda clk_n: clk_n < 1, lambda clk_n: clk_n + 1)
        fsm.add_transition("N-S:Keep Red,W-E:Green2Yellow", "N-S:Red,W-E:Green", "N-S:Red,W-E:Yellow",
                           lambda clk_n: clk_n >= 5, lambda clk_n: 1)
        fsm.add_transition("N-S:Keep Red,W-E:Keep Green", "N-S:Red,W-E:Green", "N-S:Red,W-E:Green",
                           lambda clk_n: clk_n < 5, lambda clk_n: clk_n + 1)
        fsm.add_transition("N-S:Red2Green,W-E:Yellow2Red", "N-S:Red,W-E:Yellow", "N-S:Green,W-E:Red",
                           lambda clk_n: clk_n >= 1, lambda clk_n: 1)
        fsm.add_transition("N-S:Keep Red,W-E:KeepYellow", "N-S:Red,W-E:Yellow", "N-S:Red,W-E:Yellow",
                           lambda clk_n: clk_n < 1, lambda clk_n: clk_n + 1)
        actual = fsm.execute("N-S:Green,W-E:Red", total_clk=6, clk_n=0)
        expect = {'N-S Green': False, 'N-S Yellow': True, 'N-S Red': False,
                  'W-E Green': False, 'W-E Yellow': False, 'W-E Red': True }
        self.assertEqual(actual, expect)
        actual = fsm.execute("N-S:Green,W-E:Red", total_clk=7, clk_n=0)
        expect = {'N-S Green': False, 'N-S Yellow': False, 'N-S Red': True,
                  'W-E Green': True, 'W-E Yellow': False, 'W-E Red': False, }
        self.assertEqual(actual, expect)
        actual = fsm.execute("N-S:Green,W-E:Red", total_clk=12, clk_n=0)
        expect = {'N-S Green': False, 'N-S Yellow': False, 'N-S Red': True,
                   'W-E Green': False, 'W-E Yellow': True, 'W-E Red': False }
        self.assertEqual(actual, expect)

        actual = fsm.execute("N-S:Yellow,W-E:Red", total_clk=2, clk_n=0)
        expect = {'N-S Green': False, 'N-S Yellow': False, 'N-S Red': True,
                  'W-E Green': True, 'W-E Yellow': False, 'W-E Red': False, }
        self.assertEqual(actual, expect)
        actual = fsm.execute("N-S:Yellow,W-E:Red", total_clk=10, clk_n=0)
        expect = {'N-S Green': True, 'N-S Yellow': False, 'N-S Red': False,
                  'W-E Green': False, 'W-E Yellow': False, 'W-E Red':True}
        self.assertEqual(actual, expect)

        actual = fsm.execute("N-S:Red,W-E:Green", total_clk=6, clk_n=1)
        expect = {'N-S Green': True, 'N-S Yellow': False, 'N-S Red': False,
                  'W-E Green': False, 'W-E Yellow': False, 'W-E Red':True}
        self.assertEqual(actual, expect)

        actual = fsm.execute("N-S:Red,W-E:Green", total_clk=8, clk_n=4)
        expect = {'N-S Green': False, 'N-S Yellow': True, 'N-S Red': False,
                  'W-E Green': False, 'W-E Yellow': False, 'W-E Red': True }
        self.assertEqual(actual, expect)

class NodeTest(unittest.TestCase):
    def test_state(self):
        green = State("Green",{'Green':True, 'Yellow':False, 'Red':False})
        yellow = State("Yellow", {'Green': False, 'Yellow': True, 'Red': False})
        green2yellow = Transition("Green2Yellow","Green","Yellow",lambda clk_n: clk_n >= 5, lambda clk_n: 1)
        keepGreen = Transition("Keep Green", "Green", "Green", lambda clk_n: clk_n < 5, lambda clk_n: clk_n+1)
        green.set_transition(keepGreen)
        green.set_transition(green2yellow)
        actual  = green.activate(2)
        expect = ("Green",3,keepGreen)
        self.assertEqual(actual, expect)

        actual = green.activate(5)
        expect = ("Yellow", 1, green2yellow)
        self.assertEqual(actual, expect)

    def test_None(self):
        green = State("Green", {'Green': True, 'Yellow': False, 'Red': False})
        actual = green.activate(2)
        expect = (None,None,None)
        self.assertEqual(actual, expect)



if __name__ == '__main__':
    unittest.main()