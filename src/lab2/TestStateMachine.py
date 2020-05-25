import unittest
from StateMachine import *

class FiniteStateMachineTest(unittest.TestCase):
    def test_state_machine(self):
        fsm = FiniteStateMachine("One Way Traffic Light")
        #fsm.input_port("clk",latency=1)
        #fsm.output_port("Green",latency=1)
        #fsm.output_port("Yellow",latency=1)
        #fsm.output_port("Red", latency=1)

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


if __name__ == '__main__':
    unittest.main()