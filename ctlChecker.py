import networkx as nx

class CtlChecker:
    def __init__(self, ts):
        self._callDic = {
            'true':self._satTrue,
            'ap':self._satAp,
            'and':self._satAnd,
            'or':self._satOr,
            'not':self._satNot,
            'existsNext':self._satExNext,
            'existsUntil':self._satExUntil,
            'existsAlways':self._satExAlways,
            'existsEventually':self._satExEventually,
            'forallNext':self._satFaNext,
            'forallUntil':self._satFaUntil,
            'forallAlways':self._satFaAlways,
            'forallEventually':self._satFaEventually,
            'phi':self._satPhi,
        }

        self._ts = ts

        self._orTree, self._orRoot, self._orPhi, self._orPsi = self._createOrTree()
        self._exEventuallyTree, self._exEventuallyRoot, self._exEventuallyPhi = self._createExEventuallyTree()
        self._faNextTree, self._faNextRoot, self._faNextPhi = self._createFaNextTree()
        self._faUntilTree, self._faUntilRoot, self._faUntilPhi, self._faUntilPsi = self._createFaUntilTree()
        self._faAlwaysTree, self._faAlwaysRoot, self._faAlwaysPhi = self._createFaAlwaysTree()
        self._faEventuallyTree, self._faEventuallyRoot, self._faEventuallyPhi = self._createFaEventuallyTree()

    def _createOrTree(self):
        tree = nx.DiGraph()

        #de morgan
        
        #add left not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='not')

        #add and
        nodeAnd = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd, form='and')

        #add left not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='not')

        #add right not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form='not')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form='phi', sat=set())

        tree.add_edge(nodeNot1, nodeAnd)
        tree.add_edge(nodeAnd, nodeNot2)
        tree.add_edge(nodeAnd, nodeNot3)
        tree.add_edge(nodeNot2, nodePhi)
        tree.add_edge(nodeNot3, nodePsi)
                
        return (tree, nodeNot1, nodePhi, nodePsi)

        
    def _createExEventuallyTree(self):
        tree = nx.DiGraph()

        #add exists true until phi

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form='existsUntil')

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form='true')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())

        tree.add_edge(nodeUntil, nodeTrue, son='sx')
        tree.add_edge(nodeUntil, nodePhi, son='dx')

        return (tree, nodeUntil, nodePhi)

    def _createFaNextTree(self):
        tree = nx.DiGraph()

        #add not Exists next not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='not')

        #add exist next
        nodeNext = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNext, form='existsNext')

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='not')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())

        tree.add_edge(nodeNot1, nodeNext)
        tree.add_edge(nodeNext, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)
        
        return (tree, nodeNot1, nodePhi)

    def _createFaUntilTree(self):
        tree = nx.DiGraph()

        #add a lot of states

        #add and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form='and')

        #add left not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='not')

        #add right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='not')

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form='existsUntil')

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form='existsAlways')

        #add another not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form='not')

        #add another and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form='and')

        #add one more not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form='not')

        #add even more nots
        nodeNot5 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot5, form='not')

        #add too much nots
        nodeNot6 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot6, form='not')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form='phi', sat=set())

        tree.add_edge(nodeAnd1, nodeNot1)
        tree.add_edge(nodeAnd1, nodeNot2)
        tree.add_edge(nodeNot1, nodeUntil)
        tree.add_edge(nodeNot2, nodeAlways)
        tree.add_edge(nodeUntil, nodeNot3, son='sx')
        tree.add_edge(nodeUntil, nodeAnd2, son='dx')
        tree.add_edge(nodeAlways, nodeNot4)
        tree.add_edge(nodeAnd2, nodeNot5)
        tree.add_edge(nodeAnd2, nodeNot6)
        tree.add_edge(nodeNot3, nodePsi)
        tree.add_edge(nodeNot5, nodePhi)
        tree.add_edge(nodeNot6, nodePsi)
        tree.add_edge(nodeNot4, nodePsi)
                
        return (tree, nodeAnd1, nodePhi, nodePsi)
    
    def _createFaAlwaysTree(self):
        tree = nx.DiGraph()

        #add not exists true until not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='not')

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form='existsUntil')

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form='true')

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='not')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())
        
        tree.add_edge(nodeNot1, nodeUntil)
        tree.add_edge(nodeUntil, nodeTrue, son='sx')
        tree.add_edge(nodeUntil, nodeNot2, son='dx')
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)

    def _createFaEventuallyTree(self):
        tree = nx.DiGraph()

        #add not Exists always not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='not')

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form='existsAlways')

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='not')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())
        
        tree.add_edge(nodeNot1, nodeAlways)
        tree.add_edge(nodeAlways, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)


    
    # def _subTree(self, tree, newRoot):
    #     return nx.algorithms.traversal.depth_first_search.dfs_tree(tree, newRoot)
        
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

    def _satOr(self, tree, root):
        leftSon = tree.successors(root)[0]
        rightSon = tree.successors(root)[1]
        self._orTree.node[self._orPhi]['sat'] = self._sat(tree, leftSon)
        self._orTree.node[self._orPsi]['sat'] = self._sat(tree, rightSon)
        return self._sat(self._orTree, self._orRoot)
    
    def _satExEventually(self, tree, root):
        self._exEventuallyTree.node[self._exEventuallyPhi]['sat'] = self._sat(tree, tree.successors(root)[0])
        return self._sat(self._exEventuallyTree, self._exEventuallyRoot)
    
    def _satFaNext(self, tree, root):
        self._faNextTree.node[self._faNextPhi]['sat'] = self._sat(tree, tree.successors(root)[0])
        return self._sat(self._faNextTree, self._faNextRoot)

    def _satFaUntil(self, tree, root):
        leftSon = [x for x in tree[root] if tree[root][x]['son'] == 'sx'][0]
        rightSon = [x for x in tree[root] if tree[root][x]['son'] == 'dx'][0]
        self._faUntilTree.node[self._faUntilPhi]['sat'] = self._sat(tree, leftSon)
        self._faUntilTree.node[self._faUntilPsi]['sat'] = self._sat(tree, rightSon)
        return self._sat(self._faUntilTree, self._faUntilRoot)

    def _satFaAlways(self, tree, root):
        self._faAlwaysTree.node[self._faAlwaysPhi]['sat'] = self._sat(tree, tree.successors(root)[0])
        return self._sat(self._faAlwaysTree, self._faAlwaysRoot)

    def _satFaEventually(self, tree, root):
        self._faEventuallyTree.node[self._faEventuallyPhi]['sat'] = self._sat(tree, tree.successors(root)[0])
        return self._sat(self._faEventuallyTree, self._faEventuallyRoot)

    def _satPhi(self, tree, root):
        return tree.node[root]['sat']
        
    def _sat(self, tree, root):
        if (tree.node[root]['form'] in self._callDic.keys()) :
            return self._callDic[tree.node[root]['form']](tree, root)

    def check(self, phi):
        sats = self._sat(phi.graph.copy(), [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0])
        initials = set([s for s,a in self._ts.graph.nodes(data=True) if a['initial'] ==True])
        return initials.issubset(sats)

    def sat(self, phi):
        return (self._sat(phi.graph.copy(), [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0]))
