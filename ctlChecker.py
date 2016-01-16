import conversionFactory as cf
import syntax

class CtlChecker:
    def __init__(self, ts):
        self._s = syntax.Syntax()
        
        self._callDic = {
            self._s.true          :  self._satTrue,
            self._s.ap            :  self._satAp,
            self._s.land          :  self._satAnd,
            self._s.lor           :  self._satConversionTwoSons,
            self._s.lnot          :  self._satNot,
            self._s.implies       :  self._satConversionTwoSonsOrdered,
            self._s.equals        :  self._satConversionTwoSons,
            self._s.exNext        :  self._satExNext,
            self._s.exUntil       :  self._satExUntil,
            self._s.exAlways      :  self._satExAlways,
            self._s.exEventually  :  self._satConversionOneSon,
            self._s.faNext        :  self._satConversionOneSon,
            self._s.faUntil       :  self._satConversionTwoSonsOrdered,
            self._s.faAlways      :  self._satConversionOneSon,
            self._s.faEventually  :  self._satConversionOneSon,
            self._s.exWeakUntil   :  self._satConversionTwoSonsOrdered,
            self._s.faWeakUntil   :  self._satConversionTwoSonsOrdered,
            self._s.phiNode       :  self._satPhi,
        }

        self._ts = ts

        factory = cf.ConversionFactory()
        self._convTree = dict()
        self._convRoot = dict()
        self._convPhi = dict()
        self._convPsi = dict()

        self._convTree, self._convRoot, self._convPhi, self._convPsi = factory.createConversionDictionaries()

        
        
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
        leftSon = [x for x in tree[root] if tree[root][x]['son'] == self._s.leftSon][0]
        rightSon = [x for x in tree[root] if tree[root][x]['son'] == self._s.rightSon][0]
        
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

    def _satConversionOneSon(self, tree, root):
        form = tree.node[root]['form']
        son = tree.successors(root)[0]
        
        self._convTree[form].node[self._convPhi[form]]['sat'] = self._sat(tree, son)
        return self._sat(self._convTree[form], self._convRoot[form])

    def _satConversionTwoSons(self, tree, root):
        form = tree.node[root]['form']
        leftSon = tree.successors(root)[0]
        rightSon = tree.successors(root)[1]
        
        self._convTree[form].node[self._convPhi[form]]['sat'] = self._sat(tree, leftSon)
        self._convTree[form].node[self._convPsi[form]]['sat'] = self._sat(tree, rightSon)
        return self._sat(self._convTree[form], self._convRoot[form])

    def _satConversionTwoSonsOrdered(self, tree, root):
        leftSon = [x for x in tree[root] if tree[root][x]['son'] == self._s.leftSon][0]
        rightSon = [x for x in tree[root] if tree[root][x]['son'] == self._s.rightSon][0]
        form = tree.node[root]['form']
        self._convTree[form].node[self._convPhi[form]]['sat'] = self._sat(tree, leftSon)
        self._convTree[form].node[self._convPsi[form]]['sat'] = self._sat(tree, rightSon)
        return self._sat(self._convTree[form], self._convRoot[form])

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
