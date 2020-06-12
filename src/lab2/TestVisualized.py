from src.lab2.StateMachine import *
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
fsm.execute("Green", 14)
print(fsm.visualize())