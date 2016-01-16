import networkx as nx
import syntax

class Conversions(object):
    def __init__(self):
        self._syntax = syntax.Syntax()

        self._trees = dict()
        self._roots = dict()
        self._phis = dict()
        self._psis = dict()

        self._trees[self._syntax.implies], self._roots[self._syntax.implies], self._phis[self._syntax.implies], self._psis[self._syntax.implies] = self._createImpliesTree()
        self._trees[self._syntax.equals], self._roots[self._syntax.equals], self._phis[self._syntax.equals], self._psis[self._syntax.equals] = self._createEqualTree()
        self._trees[self._syntax.lor], self._roots[self._syntax.lor], self._phis[self._syntax.lor], self._psis[self._syntax.lor] = self._createOrTree()
        self._trees[self._syntax.exEventually], self._roots[self._syntax.exEventually], self._phis[self._syntax.exEventually] = self._createExEventuallyTree()
        self._trees[self._syntax.faNext], self._roots[self._syntax.faNext], self._phis[self._syntax.faNext] = self._createFaNextTree()
        self._trees[self._syntax.faUntil], self._roots[self._syntax.faUntil], self._phis[self._syntax.faUntil], self._psis[self._syntax.faUntil] = self._createFaUntilTree()
        self._trees[self._syntax.faAlways], self._roots[self._syntax.faAlways], self._phis[self._syntax.faAlways] = self._createFaAlwaysTree()
        self._trees[self._syntax.faEventually], self._roots[self._syntax.faEventually], self._phis[self._syntax.faEventually] = self._createFaEventuallyTree()
        self._trees[self._syntax.exWeakUntil], self._roots[self._syntax.exWeakUntil], self._phis[self._syntax.exWeakUntil], self._psis[self._syntax.exWeakUntil] = self._createExistsWeakUntilTree()
        self._trees[self._syntax.faWeakUntil], self._roots[self._syntax.faWeakUntil], self._phis[self._syntax.faWeakUntil], self._psis[self._syntax.faWeakUntil] = self._createForallWeakUntilTree()

    @property
    def trees(self):
        return self._trees
    @property
    def roots(self):
        return self._roots
    @property
    def phis(self):
        return self._phis
    @property
    def psis(self):
        return self._psis
    
    def _createEqualTree(self):
        tree = nx.DiGraph()

        #!(!(a&b) & !(!a&!b))

        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add big and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._syntax.land)

        #add left not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)
        
        #add right not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._syntax.lnot)

        #add left and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._syntax.land)

        #add right and
        nodeAnd3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd3, form=self._syntax.land)

        #add right-left not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._syntax.lnot)
        
        #add right-right not
        nodeNot5 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot5, form=self._syntax.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._syntax.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeAnd1)
        tree.add_edge(nodeAnd1, nodeNot2)
        tree.add_edge(nodeAnd1, nodeNot3)
        tree.add_edge(nodeNot2, nodeAnd2)
        tree.add_edge(nodeNot3, nodeAnd3)
        tree.add_edge(nodeAnd2, nodePhi)
        tree.add_edge(nodeAnd2, nodePsi)
        tree.add_edge(nodeAnd3, nodeNot4)
        tree.add_edge(nodeAnd3, nodeNot5)
        tree.add_edge(nodeNot4, nodePhi)
        tree.add_edge(nodeNot5, nodePsi)

        return (tree, nodeNot1, nodePhi, nodePsi)
        
    def _createImpliesTree(self):
        tree = nx.DiGraph()

        #not(phi and not psi)

        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add and
        nodeAnd = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd, form=self._syntax.land)

        #add right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._syntax.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeAnd)
        tree.add_edge(nodeAnd, nodePhi)
        tree.add_edge(nodeAnd, nodeNot2)
        tree.add_edge(nodeNot2, nodePsi)
                
        return (tree, nodeNot1, nodePhi, nodePsi)

    def _createOrTree(self):
        tree = nx.DiGraph()

        #de morgan
        
        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add and
        nodeAnd = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd, form=self._syntax.land)

        #add left not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)

        #add right not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._syntax.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._syntax.phiNode, sat=set())

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
        tree.add_node(nodeUntil, form=self._syntax.exUntil)

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form=self._syntax.true)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())

        tree.add_edge(nodeUntil, nodeTrue, son=self._syntax.leftSon)
        tree.add_edge(nodeUntil, nodePhi, son=self._syntax.rightSon)

        return (tree, nodeUntil, nodePhi)

    def _createFaNextTree(self):
        tree = nx.DiGraph()

        #add not Exists next not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add exist next
        nodeNext = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNext, form=self._syntax.exNext)

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeNext)
        tree.add_edge(nodeNext, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)
        
        return (tree, nodeNot1, nodePhi)

    def _createFaUntilTree(self):
        tree = nx.DiGraph()

        #add a lot of states

        #add and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._syntax.land)

        #add left not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form=self._syntax.exUntil)

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form=self._syntax.exAlways)

        #add another not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._syntax.lnot)

        #add another and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._syntax.land)

        #add one more not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._syntax.lnot)

        #add even more nots
        nodeNot5 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot5, form=self._syntax.lnot)

        #add too much nots
        nodeNot6 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot6, form=self._syntax.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._syntax.phiNode, sat=set())

        tree.add_edge(nodeAnd1, nodeNot1)
        tree.add_edge(nodeAnd1, nodeNot2)
        tree.add_edge(nodeNot1, nodeUntil)
        tree.add_edge(nodeNot2, nodeAlways)
        tree.add_edge(nodeUntil, nodeNot3, son=self._syntax.leftSon)
        tree.add_edge(nodeUntil, nodeAnd2, son=self._syntax.rightSon)
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
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form=self._syntax.exUntil)

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form=self._syntax.true)

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        tree.add_edge(nodeNot1, nodeUntil)
        tree.add_edge(nodeUntil, nodeTrue, son=self._syntax.leftSon)
        tree.add_edge(nodeUntil, nodeNot2, son=self._syntax.rightSon)
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)

    def _createFaEventuallyTree(self):
        tree = nx.DiGraph()

        #add not Exists always not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form=self._syntax.exAlways)

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        tree.add_edge(nodeNot1, nodeAlways)
        tree.add_edge(nodeAlways, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)

    def _createExistsWeakUntilTree(self):
        tree = nx.DiGraph()

        #!((a&!b) AU (!a&!b))

        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add AU
        nodeAU = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAU, form=self._syntax.faUntil)

        #add left and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._syntax.land)

        #add right and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._syntax.land)

        #add left-right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)
        
        #add right-left not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._syntax.lnot)

        #add right-right not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._syntax.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._syntax.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeAU)
        tree.add_edge(nodeAU, nodeAnd1, son=self._syntax.leftSon)
        tree.add_edge(nodeAU, nodeAnd2, son=self._syntax.rightSon)
        tree.add_edge(nodeAnd1, nodePhi)
        tree.add_edge(nodeAnd1, nodeNot2)
        tree.add_edge(nodeNot2, nodePsi)
        tree.add_edge(nodeAnd2, nodeNot3)
        tree.add_edge(nodeAnd2, nodeNot4)        
        tree.add_edge(nodeNot3, nodePhi)
        tree.add_edge(nodeNot4, nodePsi)

        return (tree, nodeNot1, nodePhi, nodePsi)
        
    def _createForallWeakUntilTree(self):
        tree = nx.DiGraph()

        #!((a&!b) EU (!a&!b))

        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._syntax.lnot)

        #add EU
        nodeEU = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeEU, form=self._syntax.exUntil)

        #add left and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._syntax.land)

        #add right and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._syntax.land)

        #add left-right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._syntax.lnot)
        
        #add right-left not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._syntax.lnot)

        #add right-right not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._syntax.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._syntax.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._syntax.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeEU)
        tree.add_edge(nodeEU, nodeAnd1, son=self._syntax.leftSon)
        tree.add_edge(nodeEU, nodeAnd2, son=self._syntax.rightSon)
        tree.add_edge(nodeAnd1, nodePhi)
        tree.add_edge(nodeAnd1, nodeNot2)
        tree.add_edge(nodeNot2, nodePsi)
        tree.add_edge(nodeAnd2, nodeNot3)
        tree.add_edge(nodeAnd2, nodeNot4)        
        tree.add_edge(nodeNot3, nodePhi)
        tree.add_edge(nodeNot4, nodePsi)

        return (tree, nodeNot1, nodePhi, nodePsi)
        
    
