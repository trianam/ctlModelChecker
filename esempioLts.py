#!/usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx

#LTS

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

#print('a (s1): {}'.format('a' in lts.node['s1']['att']))
#print('b (s1): {}'.format('b' in lts.node['s1']['att']))
#print('c (s1): {}'.format('c' in lts.node['s1']['att']))
#print('a=b (s1): {}'.format(('a' in lts.node['s1']['att']) == ('b' in lts.node['s1']['att'])))


#labels=dict((n,{'l':n,'d':d['att']}) for n,d in lts.nodes(data=True))
#nx.draw_networkx(lts, labels=labels)



#Phi

phi = nx.DiGraph()
phi.add_node('f0', form='and')
phi.add_node('f1', form='next')
phi.add_node('f2', form='ap', val='a')
phi.add_node('f3', form='until')
phi.add_node('f4', form='ap', val='b')
phi.add_node('f5', form='allways')
phi.add_node('f6', form='not')
phi.add_node('f7', form='ap', val='c')

phi.add_edge('f0', 'f1')
phi.add_edge('f0', 'f3')
phi.add_edge('f1', 'f2')
phi.add_edge('f3', 'f4')
phi.add_edge('f3', 'f5')
phi.add_edge('f5', 'f6')
phi.add_edge('f6', 'f7')

#labels=dict((n,{'l':n,'f':d['form'],'v':(d['val'] if 'val' in d.keys() else 'ND')}) for n,d in phi.nodes(data=True))
#nx.draw_networkx(phi, labels=labels)


#plt.show()

phiTrue=nx.DiGraph()
phiTrue.add_node('f0', form='true')

def satTrue(nodo):
    return set(lts.nodes())


callDic = {
    'true':satTrue,
    }

def sat(nodo):
    if (phiTrue.node[nodo]['form'] in callDic.keys()) :
        return callDic[phiTrue.node[nodo]['form']](nodo)


print(sat('f0'))

    
