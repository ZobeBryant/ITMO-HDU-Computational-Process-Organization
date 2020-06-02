from collections import OrderedDict, namedtuple

event = namedtuple("Event", "clock, state, light")


class FiniteStateMachine(object):
    def __init__(self, name="anonymous"):
        self.name = name
        self.states = []
        self.transitions = []
        self.current_state = None
        self.event_history = []
        self.light_state_history = []

    def add_state(self, name, light):
        state = State(name, light)
        self.states.append(state)

    def add_transition(self, name, current_state, next_state, trigger, action):
        for state in self.states:
            if state.name == current_state:
                current_state = state
            if state.name == next_state:
                next_state = state
        transition = Transition(name, current_state, next_state, trigger, action)
        self.transitions.append(transition)
        for s in self.states:
            if s == current_state:
                s.set_transition(transition)

    def set_start_state(self, state_name):
        for state in self.states:
            if state.name == state_name:
                self.current_state = state
                break

    def execute(self, start_state, total_clk, clk_n=0):
        clock = 0
        self.set_start_state(start_state)
        assert self.current_state is not None
        for i in range(total_clk):
            clock = clock + 1
            self.current_state, clk_n, tr = self.current_state.activate(clk_n)
            self.light_state_history.append((clock, self.current_state.light))
            self.event_history.append((clock, tr.name, clk_n))
        return self.current_state.light


class State(object):
    def __init__(self, name, light):
        self.name = name
        self.light = light
        self.transitions = []

    def set_transition(self, transition):
        self.transitions.append(transition)

    def activate(self, clk_n):
        for tr in self.transitions:
            if tr.trigger(clk_n):
                clk_n = tr.action(clk_n)
                return tr.next_state, clk_n, tr
        return None, None, None


class Transition(object):
    def __init__(self, name, current_state, next_state, trigger, action):
        self.name = name
        self.current_state = current_state
        self.next_state = next_state
        self.trigger = trigger
        self.action = action






