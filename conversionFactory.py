import networkx as nx

class ConversionFactory:
    def createImpliesTree(self):
        tree = nx.DiGraph()

        #not(phi and not psi)

        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='!')

        #add and
        nodeAnd = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd, form='&')

        #add right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='!')
        
        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())
        
        #add psi
        nodePsi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePsi, form='phi', sat=set())

        tree.add_edge(nodeNot1, nodeAnd)
        tree.add_edge(nodeAnd, nodePhi, son='sx')
        tree.add_edge(nodeAnd, nodeNot2, son='dx')
        tree.add_edge(nodeNot2, nodePsi)
                
        return (tree, nodeNot1, nodePhi, nodePsi)

    def createOrTree(self):
        tree = nx.DiGraph()

        #de morgan
        
        #add big not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='!')

        #add and
        nodeAnd = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd, form='&')

        #add left not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='!')

        #add right not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form='!')

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

        
    def createExEventuallyTree(self):
        tree = nx.DiGraph()

        #add exists true until phi

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form='EU')

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form='true')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())

        tree.add_edge(nodeUntil, nodeTrue, son='sx')
        tree.add_edge(nodeUntil, nodePhi, son='dx')

        return (tree, nodeUntil, nodePhi)

    def createFaNextTree(self):
        tree = nx.DiGraph()

        #add not Exists next not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='!')

        #add exist next
        nodeNext = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNext, form='EX')

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='!')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())

        tree.add_edge(nodeNot1, nodeNext)
        tree.add_edge(nodeNext, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)
        
        return (tree, nodeNot1, nodePhi)

    def createFaUntilTree(self):
        tree = nx.DiGraph()

        #add a lot of states

        #add and
        nodeAnd1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd1, form='&')

        #add left not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='!')

        #add right not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='!')

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form='EU')

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form='EG')

        #add another not
        nodeNot3 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot3, form='!')

        #add another and
        nodeAnd2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAnd2, form='&')

        #add one more not
        nodeNot4 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot4, form='!')

        #add even more nots
        nodeNot5 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot5, form='!')

        #add too much nots
        nodeNot6 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot6, form='!')

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
    
    def createFaAlwaysTree(self):
        tree = nx.DiGraph()

        #add not exists true until not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='!')

        #add exists until
        nodeUntil = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeUntil, form='EU')

        #add true
        nodeTrue = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeTrue, form='true')

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='!')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())
        
        tree.add_edge(nodeNot1, nodeUntil)
        tree.add_edge(nodeUntil, nodeTrue, son='sx')
        tree.add_edge(nodeUntil, nodeNot2, son='dx')
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)

    def createFaEventuallyTree(self):
        tree = nx.DiGraph()

        #add not Exists always not phi

        #add outer not
        nodeNot1 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot1, form='!')

        #add exists always
        nodeAlways = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeAlways, form='EG')

        #add inner not
        nodeNot2 = nx.utils.misc.generate_unique_node()
        tree.add_node(nodeNot2, form='!')

        #add phi
        nodePhi = nx.utils.misc.generate_unique_node()
        tree.add_node(nodePhi, form='phi', sat=set())
        
        tree.add_edge(nodeNot1, nodeAlways)
        tree.add_edge(nodeAlways, nodeNot2)
        tree.add_edge(nodeNot2, nodePhi)

        return (tree, nodeNot1, nodePhi)

