#import networkx as nx

class CtlChecker:
    def __init__(self, ts):
        self._callDic = {
            'true':self._satTrue,
            'ap':self._satAp,
            'and':self._satAnd,
            'not':self._satNot,
            'existsNext':self._satExNext,
            'existsUntil':self._satExUntil,
            'existsAlways':self._satExAlways,
            'existsEventually':self._satExEventually,
            'forallNext':self._satFaNext,
            'forallUntil':self._satFaUntil,
            'forallAlways':self._satFaAlways,
            'forallEventually':self._satFaEventually,
        }

        self._ts = ts

    def _subTree(self, tree, newRoot):
        return nx.algorithms.traversal.depth_first_search.dfs_tree(tree, newRoot)
        
    def _satTrue(self, tree, root):
        return set(self._ts.graph.nodes())

    def _satAp(self, tree, root):
        retSet = set()
        for stato,att in self._ts.graph.nodes(data=True):
            if tree.node[root]['val'] in att['att']:
               retSet.add(stato)

        return retSet

    def _satAnd(self, tree, root):
        rootA = tree.successors(root)[0]
        rootB = tree.successors(root)[1]
        
        return self._sat(tree, rootA).intersection(self._sat(tree, rootB))

    def _satNot(self, tree, root):
        return set(self._ts.graph.nodes()).difference(self._sat(tree, tree.successors(root)[0]))

    def _satExNext(self, tree, root):
        retSet = set()
        satPhi = self._sat(tree, tree.successors(root)[0])

        for stato in self._ts.graph.nodes():
            if set(self._ts.graph.successors(stato)).intersection(satPhi): #true if not empty
                retSet.add(stato)

        return retSet

    def _satExUntil(self, tree, root):
        leftSon = [x for x in tree[root] if tree[root][x]['son'] == 'sx'][0]
        rightSon = [x for x in tree[root] if tree[root][x]['son'] == 'dx'][0]
        
        E = self._sat(tree, rightSon)
        T = E.copy()

        while E: #while not empty
            r = E.pop()
            for s in self._ts.graph.predecessors(r):
                if s in self._sat(tree, leftSon).difference(T):
                    E.add(s)
                    T.add(s)
        return T


    def _satExAlways(self, tree, root):
        T = self._sat(tree, tree.successors(root)[0])
        E = set(self._ts.graph.nodes()).difference(T)
        count = dict()
        for s in T:
            count[s] = len(self._ts.graph.successors(s))

        while E:
            r = E.pop()
            for s in self._ts.graph.predecessors(r):
                if s in T:
                    count[s] = count[s]-1
                    if count[s] == 0:
                        T.remove(s)
                        E.add(s)

        return T

    def _satExEventually(self, tree, root):
        #add exists true until phi
        #add true
        newNodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeTrue, form='true')

        #add exists until
        newNodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeUntil, form='existsUntil')
        tree.add_edge(newNodeUntil, newNodeTrue, son='sx')
        tree.add_edge(newNodeUntil, tree.node(root).successors()[0], son='dx')
        
        return _sat(tree, newNodeUntil)
    
    def _satFaNext(self, tree, root):
        #add not Exists next not phi
        #add inner not
        newNodeNot = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeNot, form='not')
        tree.add_edge(newNodeNot, tree.node(root).successors()[0])

        #add exist next
        newNodeNext = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeNext, form='existsNext')
        tree.add_edge(newNodeNext, newNodeNot)
        
        #add outer not
        newNodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeNot2, form='not')
        tree.add_edge(newNodeNot2, newNodeNext)
        
        return _sat(tree, newNodeNot2)

    def _satFaUntil(self, tree, root):
        leftSon = [x for x in tree[root] if tree[root][x]['son'] == 'sx'][0]
        rightSon = [x for x in tree[root] if tree[root][x]['son'] == 'dx'][0]

        return

    def _satFaAlways(self, tree, root):
        #add not exists true until not phi
        #add inner not
        newNodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeNot1, form='not')
        tree.add_edge(newNodeNot1, tree.node(root).successors()[0])

        #add true
        newNodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeTrue, form='true')

        #add exists until
        newNodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeUntil, form='existsUntil')
        tree.add_edge(newNodeUntil, newNodeTrue, son='sx')
        tree.add_edge(newNodeUntil, newNodeNot1, son='dx')
        
        #add outer not
        newNodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeNot2, form='not')
        tree.add_edge(newNodeNot2, newNodeUntil)

        return _sat(tree, newNodeNot2)

    def _satFaEventually(self, tree, root):
        #add not Exists eventually not phi
        #add inner not
        newNodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeNot1, form='not')
        tree.add_edge(newNodeNot1, tree.node(root).successors()[0])

        #add exists always
        newNodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeAlways, form='existsAlways')
        tree.add_edge(newNodeAlways, newNodeNot1)
        
        #add outer not
        newNodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(newNodeNot2, form='not')
        tree.add_edge(newNodeNot2, newNodeAlways)
        
        return _sat(tree, newNodeNot2)

    def _sat(self, tree, root):
        if (tree.node[root]['form'] in self._callDic.keys()) :
            return self._callDic[tree.node[root]['form']](tree, root)

    def check(self, phi):
        sats = self._sat(phi.graph.copy(), [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0])
        initials = set([s for s,a in self._ts.graph.nodes(data=True) if a['initial'] ==True])
        return initials.issubset(sats)

    def sat(self, phi):
        return (self._sat(phi.graph.copy(), [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0]))
