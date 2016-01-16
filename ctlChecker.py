import conversions
import syntax

class CtlChecker:
    def __init__(self, ts):
        self._syntax = syntax.Syntax()
        self._conv = conversions.Conversions()
        self._ts = ts
        
        self._callDic = {
            self._syntax.true          :  self._satTrue,
            self._syntax.ap            :  self._satAp,
            self._syntax.land          :  self._satAnd,
            self._syntax.lor           :  self._satConversionTwoSons,
            self._syntax.lnot          :  self._satNot,
            self._syntax.implies       :  self._satConversionTwoSonsOrdered,
            self._syntax.equals        :  self._satConversionTwoSons,
            self._syntax.exNext        :  self._satExNext,
            self._syntax.exUntil       :  self._satExUntil,
            self._syntax.exAlways      :  self._satExAlways,
            self._syntax.exEventually  :  self._satConversionOneSon,
            self._syntax.faNext        :  self._satConversionOneSon,
            self._syntax.faUntil       :  self._satConversionTwoSonsOrdered,
            self._syntax.faAlways      :  self._satConversionOneSon,
            self._syntax.faEventually  :  self._satConversionOneSon,
            self._syntax.exWeakUntil   :  self._satConversionTwoSonsOrdered,
            self._syntax.faWeakUntil   :  self._satConversionTwoSonsOrdered,
            self._syntax.phiNode       :  self._satPhi,
        }

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
        leftSon = [x for x in tree[root] if tree[root][x]['son'] == self._syntax.leftSon][0]
        rightSon = [x for x in tree[root] if tree[root][x]['son'] == self._syntax.rightSon][0]
        
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
        
        self._conv.trees[form].node[self._conv.phis[form]]['sat'] = self._sat(tree, son)
        return self._sat(self._conv.trees[form], self._conv.roots[form])

    def _satConversionTwoSons(self, tree, root):
        form = tree.node[root]['form']
        leftSon = tree.successors(root)[0]
        rightSon = tree.successors(root)[1]
        
        self._conv.trees[form].node[self._conv.phis[form]]['sat'] = self._sat(tree, leftSon)
        self._conv.trees[form].node[self._conv.psis[form]]['sat'] = self._sat(tree, rightSon)
        return self._sat(self._conv.trees[form], self._conv.roots[form])

    def _satConversionTwoSonsOrdered(self, tree, root):
        form = tree.node[root]['form']
        leftSon = [x for x in tree[root] if tree[root][x]['son'] == self._syntax.leftSon][0]
        rightSon = [x for x in tree[root] if tree[root][x]['son'] == self._syntax.rightSon][0]
        
        self._conv.trees[form].node[self._conv.phis[form]]['sat'] = self._sat(tree, leftSon)
        self._conv.trees[form].node[self._conv.psis[form]]['sat'] = self._sat(tree, rightSon)
        return self._sat(self._conv.trees[form], self._conv.roots[form])

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
