from collections import OrderedDict, namedtuple
from functools import wraps
event = namedtuple("Event", "clock, state, light")

def accepts():
    def arg_type(f):
        @wraps(f)
        def new_f(*args):
            if type(args[1])!=str:
               return("positional argument 1 should be a string")
            return f(*args)
        return new_f

    return arg_type

def accepts_add_state():
    def arg_type(f):
        @wraps(f)
        def new_f(*args):
            if type(args[1])!=str:
                return("positional argument 1 should be a string")
            if type(args[2])!=dict:
               return("positional argument 2 should be a type of dict")
            return f(*args)
        return new_f

    return arg_type

def accepts_add_transition():
    def arg_type(f):
        @wraps(f)
        def new_f(*args):
            if type(args[1])!=str:
               return("positional argument 1 should be a string")
            if type(args[2])!=str:
               return("positional argument 2 should be a string")
            if type(args[3])!=str:
               return("positional argument 3 should be a string")
            if not hasattr(args[4],"__call__"):
                return("positional argument 4 should be a function")
            if not hasattr(args[5],"__call__"):
                return ("positional argument 5 should be a function")

            return f(*args)
        return new_f

    return arg_type

def accepts_set_transition(f):
    @wraps(f)
    def new_f(*args):
        if type(args[1])!=Transition:
            return ("positional argument 1 should be a type of Transition")
        return f(*args)
    return new_f

    return arg_type

def accepts_activate(f):
    @wraps(f)
    def new_f(*args):
        if type(args[1])!=int:
            return("positional argument 1 should be a type of int")
        return f(*args)

    return new_f

def accepts_execute():
    def arg_type(f):
        @wraps(f)
        def new_f(*args):
            #print(args)
            if type(args[1])!=str:
               return ("positional argument 1 should be a string")
            if type(args[2])!=int:
               return ("positional argument 2 should be a type of int")
            return f(*args)
        return new_f

    return arg_type

class FiniteStateMachine(object):
    def __init__(self, name="anonymous"):
        self.name = name
        self.states = []
        self.transitions = []
        self.current_state = None
        self.event_history = []
        self.light_state_history = []


    @accepts_add_state()
    def add_state(self, name, light):
        state = State(name, light)
        self.states.append(state)

    @accepts_add_transition()
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

    @accepts()
    def set_start_state(self, state_name):
        for state in self.states:
            if state.name == state_name:
                self.current_state = state
                break

    @accepts_execute()
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

    def visualize(self):
        res = []
        res.append("digraph G {")
        res.append(" traffic light;")
        res.append(" --------")
        res.append(" init_state--->start")
        for i, s in enumerate(self.states):
            res.append(' state_{}[label="{}"];'.format(i, s.name))
        res.append(" init_state--->end")
        res.append(" --------")
        res.append(" run--->start")
        for i in range(len(self.event_history)):
            if self.light_state_history[i][1]["Green"]==True:
                res.append('clock_{}  state_0[label=Green]--Transition-->{}'.format(i,self.event_history[i][1]))
            elif self.light_state_history[i][1]["Yellow"] == True:
                res.append('clock_{}  state_1[label=Yellow]--Transition-->{}'.format(i,self.event_history[i][1]))
            else:
                res.append('clock_{}  state_2[label=Red]--Transition-->{}'.format(i,self.event_history[i][1]))
        res.append(" run--->end")
        res.append(" --------")
        res.append("}")
        return "\n".join(res)


class State(object):
    def __init__(self, name, light):
        self.name = name
        self.light = light
        self.transitions = []

    @accepts_set_transition
    def set_transition(self, transition):
        self.transitions.append(transition)

    @accepts_activate
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






