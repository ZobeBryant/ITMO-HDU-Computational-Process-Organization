from graphviz import Digraph

g = Digraph('Traffic light')
g.node(name='State0',color='green')
g.node(name='State1',color='yellow')
g.node(name='State2',color='red')
g.edge('State0','State0',"Keep Green[trigger()/action()]",color='green')
g.edge('State0','State1',"Green2Yellow[trigger()/action()]",color='yellow')
g.edge('State1','State1',"Keep Yellow[trigger()/action()]",color='yellow')
g.edge('State1','State2',"Yellow2Red[trigger()/action()]",color='red')
g.edge('State2','State2',"Keep Red[trigger()/action()]",color='red')
g.edge('State2','State0',"Red2Greem[trigger()/action()]",color='green')
g.view()
