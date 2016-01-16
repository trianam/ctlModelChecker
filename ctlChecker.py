import conversions
import syntax

class CtlChecker:
    """
    Main class, used for starting the computation of the satisfation
    set and for model check a CTL formula with the linked transition
    system. In the costructor is passed the linked transition system.
    """
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

    def _satTrue(self, tree, currNode):
        """
        Return satisfation set for 'true', that is all the nodes of
        the transition system.
        """
        return set(self._ts.graph.nodes())

    def _satAp(self, tree, currNode):
        """
        Return satisfation set for an atomic proposition, that is all
        the nodes of the transition system that contain that atom.
        """
        retSet = set()
        for stato,att in self._ts.graph.nodes(data=True):
            if tree.node[currNode]['val'] in att['att']:
               retSet.add(stato)

        return retSet

    def _satAnd(self, tree, currNode):
        """
        Return satisfation set for 'phi and psi', that is the
        intersection of the satisfation sets of phi and psi.
        """
        sonA = tree.successors(currNode)[0]
        sonB = tree.successors(currNode)[1]
        
        return self._sat(tree, sonA).intersection(self._sat(tree, sonB))

    def _satNot(self, tree, currNode):
        """
        Return satisfation set for 'not phi', that is the complement
        of the satisfation set of phi.
        """
        return set(self._ts.graph.nodes()).difference(self._sat(tree, tree.successors(currNode)[0]))

    def _satExNext(self, tree, currNode):
        """
        Return satisfation set for 'EX phi', that is the set of nodes that
        have a successor that satisfy phi.
        """
        retSet = set()
        satPhi = self._sat(tree, tree.successors(currNode)[0])

        for stato in self._ts.graph.nodes():
            if set(self._ts.graph.successors(stato)).intersection(satPhi): #true if not empty
                retSet.add(stato)

        return retSet

    def _satExUntil(self, tree, currNode):
        """
        Return satisfation set for 'E(phi U psi)', that is the set of nodes that
        have a track that satisfy phi ended by a state that satisfy
        psi. This set is calculated going backward starting from the
        states that satisfy psi, adding the states that satisfy phi
        and have an edge to the already found states.
        """
        leftSon = [x for x in tree[currNode] if tree[currNode][x]['son'] == self._syntax.leftSon][0]
        rightSon = [x for x in tree[currNode] if tree[currNode][x]['son'] == self._syntax.rightSon][0]

        S = self._sat(tree, leftSon)
        E = self._sat(tree, rightSon)
        T = E.copy()

        while E: #while not empty
            r = E.pop()
            for s in self._ts.graph.predecessors(r):
                if s in S.difference(T):
                    E.add(s)
                    T.add(s)
        return T


    def _satExAlways(self, tree, currNode):
        """
        Return satisfation set for 'EG phi', that is the set of nodes
        that have a track that satisfy always phi. This set is
        calculated using counters that start with the numbers of
        neighbours for each state that satisfy phi, and then remove a
        state from the set only if every neighbour don't satisfy phi.
        """
        
        T = self._sat(tree, tree.successors(currNode)[0])
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

    def _satConversionOneSon(self, tree, currNode):
        """
        Return satisfation set for every conversion tree that has only
        one son phi. That is calculated saving the satisfation set of
        phi in a special node of the conversion tree before calling
        the calculus.
        """
        form = tree.node[currNode]['form']
        son = tree.successors(currNode)[0]
        
        self._conv.trees[form].node[self._conv.phis[form]]['sat'] = self._sat(tree, son)
        return self._sat(self._conv.trees[form], self._conv.roots[form])

    def _satConversionTwoSons(self, tree, currNode):
        """
        Return satisfation set for every conversion tree that has two
        sons phi and psi. That is calculated saving the satisfation
        sets of phi and psi in special nodes of the conversion tree
        before calling the calculus.
        """
        form = tree.node[currNode]['form']
        sonA = tree.successors(currNode)[0]
        sonB = tree.successors(currNode)[1]
        
        self._conv.trees[form].node[self._conv.phis[form]]['sat'] = self._sat(tree, sonA)
        self._conv.trees[form].node[self._conv.psis[form]]['sat'] = self._sat(tree, sonB)
        return self._sat(self._conv.trees[form], self._conv.roots[form])

    def _satConversionTwoSonsOrdered(self, tree, currNode):
        """
        Return satisfation set for every conversion tree that has two
        sons phi and psi whit a proper order. That is calculated
        saving the satisfation sets of phi and psi in special nodes of
        the conversion tree before calling the calculus.
        """
        form = tree.node[currNode]['form']
        leftSon = [x for x in tree[currNode] if tree[currNode][x]['son'] == self._syntax.leftSon][0]
        rightSon = [x for x in tree[currNode] if tree[currNode][x]['son'] == self._syntax.rightSon][0]
        
        self._conv.trees[form].node[self._conv.phis[form]]['sat'] = self._sat(tree, leftSon)
        self._conv.trees[form].node[self._conv.psis[form]]['sat'] = self._sat(tree, rightSon)
        return self._sat(self._conv.trees[form], self._conv.roots[form])

    def _satPhi(self, tree, currNode):
        """
        Return satisfation set for the special node of the conversion
        tree. Basically returns only the previously saved content.
        """
        return tree.node[currNode]['sat']
        
    def _sat(self, tree, currNode):
        """
        The generic function for the calculus of the satisfaction set
        of a formula. It uses a dictionary for calling the right
        function for the type of formula.
        """
        if (tree.node[currNode]['form'] in self._callDic.keys()) :
            return self._callDic[tree.node[currNode]['form']](tree, currNode)

    def sat(self, phi):
        """
        The function that compute the satisfaction set of a formula
        and is callable by outside the class. Basically it calls _sat
        initializing the current node with the root of the formula.
        """
        return self._sat(phi.graph.copy(), [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0])

    def check(self, phi):
        """
        The function that do the model checking. It check if all the
        initial states of the transition system are contained inside
        the calculated satisfation set.
        """
        sats = self.sat(phi)
        initials = set([s for s,a in self._ts.graph.nodes(data=True) if a['initial'] ==True])
        return initials.issubset(sats)

