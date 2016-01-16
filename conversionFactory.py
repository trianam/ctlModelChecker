import networkx as nx
import syntax

class ConversionFactory:
    def __init__(self):
        self._s = syntax.Syntax()

    def createConversionDictionaries(self):
        convTree = dict()
        convRoot = dict()
        convPhi = dict()
        convPsi = dict()

        convTree[self._s.implies], convRoot[self._s.implies], convPhi[self._s.implies], convPsi[self._s.implies] = self._createImpliesTree()
        convTree[self._s.equals], convRoot[self._s.equals], convPhi[self._s.equals], convPsi[self._s.equals] = self._createEqualTree()
        convTree[self._s.lor], convRoot[self._s.lor], convPhi[self._s.lor], convPsi[self._s.lor] = self._createOrTree()
        convTree[self._s.exEventually], convRoot[self._s.exEventually], convPhi[self._s.exEventually] = self._createExEventuallyTree()
        convTree[self._s.faNext], convRoot[self._s.faNext], convPhi[self._s.faNext] = self._createFaNextTree()
        convTree[self._s.faUntil], convRoot[self._s.faUntil], convPhi[self._s.faUntil], convPsi[self._s.faUntil] = self._createFaUntilTree()
        convTree[self._s.faAlways], convRoot[self._s.faAlways], convPhi[self._s.faAlways] = self._createFaAlwaysTree()
        convTree[self._s.faEventually], convRoot[self._s.faEventually], convPhi[self._s.faEventually] = self._createFaEventuallyTree()
        convTree[self._s.exWeakUntil], convRoot[self._s.exWeakUntil], convPhi[self._s.exWeakUntil], convPsi[self._s.exWeakUntil] = self._createExistsWeakUntilTree()
        convTree[self._s.faWeakUntil], convRoot[self._s.faWeakUntil], convPhi[self._s.faWeakUntil], convPsi[self._s.faWeakUntil] = self._createForallWeakUntilTree()
        return(convTree, convRoot, convPhi, convPsi)


    def _createEqualTree(self):
        tree = nx.DiGraph()

        #!(!(a&b) & !(!a&!b))

        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add big and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._s.land)

        #add left not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)
        
        #add right not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._s.lnot)

        #add left and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._s.land)

        #add right and
        nodeAnd3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd3, form=self._s.land)

        #add right-left not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._s.lnot)
        
        #add right-right not
        nodeNot5 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot5, form=self._s.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._s.phiNode, sat=set())

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
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add and
        nodeAnd = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd, form=self._s.land)

        #add right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._s.phiNode, sat=set())

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
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add and
        nodeAnd = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd, form=self._s.land)

        #add left not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)

        #add right not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._s.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._s.phiNode, sat=set())

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
        tree.add_node(nodeUntil, form=self._s.exUntil)

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form=self._s.true)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())

        tree.add_edge(nodeUntil, nodeTrue, son=self._s.leftSon)
        tree.add_edge(nodeUntil, nodePhi, son=self._s.rightSon)

        return (tree, nodeUntil, nodePhi)

    def _createFaNextTree(self):
        tree = nx.DiGraph()

        #add not Exists next not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add exist next
        nodeNext = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNext, form=self._s.exNext)

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeNext)
        tree.add_edge(nodeNext, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)
        
        return (tree, nodeNot1, nodePhi)

    def _createFaUntilTree(self):
        tree = nx.DiGraph()

        #add a lot of states

        #add and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._s.land)

        #add left not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form=self._s.exUntil)

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form=self._s.exAlways)

        #add another not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._s.lnot)

        #add another and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._s.land)

        #add one more not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._s.lnot)

        #add even more nots
        nodeNot5 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot5, form=self._s.lnot)

        #add too much nots
        nodeNot6 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot6, form=self._s.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._s.phiNode, sat=set())

        tree.add_edge(nodeAnd1, nodeNot1)
        tree.add_edge(nodeAnd1, nodeNot2)
        tree.add_edge(nodeNot1, nodeUntil)
        tree.add_edge(nodeNot2, nodeAlways)
        tree.add_edge(nodeUntil, nodeNot3, son=self._s.leftSon)
        tree.add_edge(nodeUntil, nodeAnd2, son=self._s.rightSon)
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
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form=self._s.exUntil)

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form=self._s.true)

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        tree.add_edge(nodeNot1, nodeUntil)
        tree.add_edge(nodeUntil, nodeTrue, son=self._s.leftSon)
        tree.add_edge(nodeUntil, nodeNot2, son=self._s.rightSon)
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)

    def _createFaEventuallyTree(self):
        tree = nx.DiGraph()

        #add not Exists always not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form=self._s.exAlways)

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        tree.add_edge(nodeNot1, nodeAlways)
        tree.add_edge(nodeAlways, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)

    def _createExistsWeakUntilTree(self):
        tree = nx.DiGraph()

        #!((a&!b) AU (!a&!b))

        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add AU
        nodeAU = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAU, form=self._s.faUntil)

        #add left and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._s.land)

        #add right and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._s.land)

        #add left-right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)
        
        #add right-left not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._s.lnot)

        #add right-right not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._s.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._s.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeAU)
        tree.add_edge(nodeAU, nodeAnd1, son=self._s.leftSon)
        tree.add_edge(nodeAU, nodeAnd2, son=self._s.rightSon)
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
        tree.add_node(nodeNot1, form=self._s.lnot)

        #add EU
        nodeEU = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeEU, form=self._s.exUntil)

        #add left and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form=self._s.land)

        #add right and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form=self._s.land)

        #add left-right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form=self._s.lnot)
        
        #add right-left not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form=self._s.lnot)

        #add right-right not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form=self._s.lnot)
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form=self._s.phiNode, sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form=self._s.phiNode, sat=set())

        tree.add_edge(nodeNot1, nodeEU)
        tree.add_edge(nodeEU, nodeAnd1, son=self._s.leftSon)
        tree.add_edge(nodeEU, nodeAnd2, son=self._s.rightSon)
        tree.add_edge(nodeAnd1, nodePhi)
        tree.add_edge(nodeAnd1, nodeNot2)
        tree.add_edge(nodeNot2, nodePsi)
        tree.add_edge(nodeAnd2, nodeNot3)
        tree.add_edge(nodeAnd2, nodeNot4)        
        tree.add_edge(nodeNot3, nodePhi)
        tree.add_edge(nodeNot4, nodePsi)

        return (tree, nodeNot1, nodePhi, nodePsi)
        
    
