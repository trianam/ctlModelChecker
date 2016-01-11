#!/usr/bin/python
#provagithub
import matplotlib.pyplot as plt
import networkx as nx

lts=nx.DiGraph()

lts.add_node('s0',att=['a','b','c'])
lts.add_node('s1',att=['a','b'])
lts.add_node('s2',att=['b','c'])
lts.add_node('s3',att=['a'])
lts.add_node('s4',att=['b'])
lts.add_node('s5',att=['a','c'])
lts.add_node('s6',att=['c'])
lts.add_node('s7',att=[])

lts.add_edge('s0', 's2')
lts.add_edge('s1', 's3')
lts.add_edge('s2', 's0')
lts.add_edge('s2', 's1')
lts.add_edge('s3', 's0')
lts.add_edge('s4', 's0')
lts.add_edge('s4', 's1')
lts.add_edge('s5', 's1')
lts.add_edge('s5', 's7')
lts.add_edge('s6', 's4')
lts.add_edge('s7', 's3')
lts.add_edge('s7', 's6')

print('a (s1): {}'.format('a' in lts.node['s1']['att']))
print('b (s1): {}'.format('b' in lts.node['s1']['att']))
print('c (s1): {}'.format('c' in lts.node['s1']['att']))
print('a=b (s1): {}'.format(('a' in lts.node['s1']['att']) == ('b' in lts.node['s1']['att'])))


labels=dict((n,{'l':n,'d':d['att']}) for n,d in lts.nodes(data=True))
nx.draw_networkx(lts, labels=labels)
#plt.show()
