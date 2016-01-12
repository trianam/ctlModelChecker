#!/usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx

#LTS

lts=nx.DiGraph()

lts.add_node('s0',att=['a','b','c'],initial=False)
lts.add_node('s1',att=['a','b'],initial=True)
lts.add_node('s2',att=['b','c'],initial=False)
lts.add_node('s3',att=['a'],initial=False)
lts.add_node('s4',att=['b'],initial=False)
lts.add_node('s5',att=['a','c'],initial=False)
lts.add_node('s6',att=['c'],initial=False)
lts.add_node('s7',att=[],initial=False)

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

# phi = nx.DiGraph()
# phi.add_node('f0', root=True, form='and')
# phi.add_node('f1', root=False, form='next')
# phi.add_node('f2', root=False, form='ap', val='a')
# phi.add_node('f3', root=False, form='until')
# phi.add_node('f4', root=False, form='ap', val='b')
# phi.add_node('f5', root=False, form='always')
# phi.add_node('f6', root=False, form='not')
# phi.add_node('f7', root=False, form='ap', val='c')

# phi.add_edge('f0', 'f1')
# phi.add_edge('f0', 'f3')
# phi.add_edge('f1', 'f2')
# phi.add_edge('f3', 'f4')
# phi.add_edge('f3', 'f5')
# phi.add_edge('f5', 'f6')
# phi.add_edge('f6', 'f7')

#labels=dict((n,{'l':n,'f':d['form'],'v':(d['val'] if 'val' in d.keys() else 'ND')}) for n,d in phi.nodes(data=True))
#nx.draw_networkx(phi, labels=labels)


#plt.show()

# phi=nx.DiGraph()
# phi.add_node('f0', root=True, form='and')
# phi.add_node('f1', root=False, form='ap', val='a')
# phi.add_node('f2', root=False, form='not')
# phi.add_node('f3', root=False, form='ap', val='b')

# phi.add_edge('f0','f1')
# phi.add_edge('f0','f2')
# phi.add_edge('f2','f3')

phi = nx.DiGraph()
phi.add_node('f0', root=True, form='until')
phi.add_node('f1', root=False, form='true')
phi.add_node('f2', root=False, form='and')
phi.add_node('f3', root=False, form='not')
phi.add_node('f4', root=False, form='not')
phi.add_node('f5', root=False, form='and')
phi.add_node('f6', root=False, form='and')
phi.add_node('f7', root=False, form='not')
phi.add_node('f8', root=False, form='not')
phi.add_node('f9', root=False, form='not')
phi.add_node('f10', root=False, form='not')
phi.add_node('f11', root=False, form='and')
phi.add_node('f12', root=False, form='not')
phi.add_node('f13', root=False, form='not')
phi.add_node('f14', root=False, form='and')
phi.add_node('f15', root=False, form='and')
phi.add_node('f16', root=False, form='ap', val='a')
phi.add_node('f17', root=False, form='ap', val='c')
phi.add_node('f18', root=False, form='ap', val='a')
phi.add_node('f19', root=False, form='ap', val='c')
phi.add_node('f20', root=False, form='ap', val='a')
phi.add_node('f21', root=False, form='not')
phi.add_node('f22', root=False, form='not')
phi.add_node('f23', root=False, form='ap', val='b')
phi.add_node('f24', root=False, form='ap', val='b')
phi.add_node('f25', root=False, form='ap', val='a')
phi.add_node('f26', root=False, form='and')

phi.add_edge('f0','f1')
phi.add_edge('f0','f2')
phi.add_edge('f2','f3')
phi.add_edge('f2','f4')
phi.add_edge('f3','f5')
phi.add_edge('f4','f6')
phi.add_edge('f5','f7')
phi.add_edge('f5','f8')
phi.add_edge('f6','f9')
phi.add_edge('f6','f10')
phi.add_edge('f7','f11')
phi.add_edge('f8','f26')
phi.add_edge('f9','f14')
phi.add_edge('f10','f15')
phi.add_edge('f11','f16')
phi.add_edge('f11','f17')
phi.add_edge('f26','f12')
phi.add_edge('f26','f13')
phi.add_edge('f14','f20')
phi.add_edge('f14','f21')
phi.add_edge('f15','f22')
phi.add_edge('f15','f23')
phi.add_edge('f12','f18')
phi.add_edge('f13','f19')
phi.add_edge('f21','f24')
phi.add_edge('f22','f25')


def satTrue(nodo):
    return set(lts.nodes())

def satAp(nodo):
    retSet = set()
    for stato,att in lts.nodes(data=True):
        if phi.node[nodo]['val'] in att['att']:
           retSet.add(stato)

    return retSet

def satAnd(nodo):
    return sat(phi.successors(nodo)[0]).intersection(sat(phi.successors(nodo)[1]))

def satNot(nodo):
    return set(lts.nodes()).difference(sat(phi.successors(nodo)[0]))
    
def satNext(nodo):
    retSet = set()
    satPhi = sat(phi.successors(nodo)[0])

    for stato in lts.nodes():
        if set(lts.successors(stato)).intersection(satPhi): #true if not empty
            retSet.add(stato)

    return retSet

def satUntil(nodo):
    E = sat(phi.successors(nodo)[1])
    T = E.copy()

    while E: #while not empty
        r = E.pop()
        for s in lts.predecessors(r):
            if s in sat(phi.successors(nodo)[0]).difference(T):
                E.add(s)
                T.add(s)
    return T
        

def satAlways(nodo):
    T = sat(phi.successors(nodo)[0])
    E = set(lts.nodes()).difference(T)
    count = dict()
    for s in T:
        count[s] = len(lts.successors(s))

    while E:
        r = E.pop()
        for s in lts.predecessors(r):
            if s in T:
                count[s] = count[s]-1
                if count[s] == 0:
                    T.remove(s)
                    E.add(s)

    return T

callDic = {
    'true':satTrue,
    'ap':satAp,
    'and':satAnd,
    'not':satNot,
    'next':satNext,
    'until':satUntil,
    'always':satAlways,
    }

def sat(nodo):
    if (phi.node[nodo]['form'] in callDic.keys()) :
        return callDic[phi.node[nodo]['form']](nodo)

def checkLts():
    sats = sat('f0')
    for s in sats:
        if lts.node[s]['initial']:
            return True
    return False

print(checkLts())

    
