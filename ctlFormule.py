import matplotlib.pyplot as plt
import networkx as nx
import pyparsing as pp
import syntax

class CtlFormule(object):
    """
    Class that contains the tree for a CTL formula parsed from a
    configuration file passed during costruction.
    """

    _syntax = syntax.Syntax()
    _atom = pp.Word(pp.alphas)
    _true = pp.Literal(_syntax.true)
    _op = _atom | _true

    _form = pp.operatorPrecedence( _op, [
        (_syntax.lnot, 1, pp.opAssoc.RIGHT),
        (pp.oneOf(_syntax.land+' '+_syntax.lor), 2, pp.opAssoc.LEFT),
        (pp.oneOf(_syntax.implies+' '+_syntax.equals), 2, pp.opAssoc.LEFT),
        (pp.oneOf(_syntax.exNext+' '+_syntax.exAlways+' '+_syntax.exEventually+' '+_syntax.faNext+' '+_syntax.faAlways+' '+_syntax.faEventually), 1, pp.opAssoc.RIGHT),
        (pp.oneOf(_syntax.exUntil+' '+_syntax.faUntil+' '+_syntax.exWeakUntil+' '+_syntax.faWeakUntil), 2, pp.opAssoc.LEFT)])

    
    def __init__(self, string, loadFromFile=False):
        self._graph = nx.DiGraph()
        if loadFromFile:
            self._loadFromFile(string)
        else:
            self._parseNode(self._form.parseString(string)[0], isRoot=True)
        
    def _parseNode(self, nodeList, isRoot=False):
        newId = nx.utils.misc.generate_unique_node()
        if isinstance(nodeList, str):
            if nodeList == self._syntax.true:
                self._graph.add_node(newId, root=isRoot, form=self._syntax.true)
            else:
                self._graph.add_node(newId, root=isRoot, form=self._syntax.ap, val=nodeList)
            
        elif len(nodeList) == 2:
            self._graph.add_node(newId, root=isRoot, form=nodeList[0])
            self._graph.add_edge(newId, self._parseNode(nodeList[1]))
        else: #len(nodeList) == 3
            self._graph.add_node(newId, root=isRoot, form=nodeList[1])
            self._graph.add_edge(newId, self._parseNode(nodeList[0]), son=self._syntax.leftSon)
            self._graph.add_edge(newId, self._parseNode(nodeList[2]), son=self._syntax.rightSon)

        return newId

    def _loadFromFile(self, filename):
        f = open(filename, 'r')
        nodesPart = True
        firstLine = True
        for line in f:
            fields = line.split('//')[0].split()
            if nodesPart and len(fields) == 0:
                nodesPart = False
                continue

            if nodesPart:
                if (fields[1] == self._syntax.ap):
                    self._graph.add_node(fields[0], root=firstLine, form=fields[1], val=fields[2])
                else:
                    self._graph.add_node(fields[0], root=firstLine, form=fields[1])
                firstLine = False

            else:
                if len(fields) == 3:
                    self._graph.add_edge(fields[0], fields[1], son=fields[2])
                else:
                    self._graph.add_edge(fields[0], fields[1])

    
    def draw(self):
        labels=dict((n,{'l':n,'d':d['form']}) for n,d in self._graph.nodes(data=True))
        nx.draw_networkx(self._graph, labels=labels)
        plt.show()

    @property
    def graph(self):
        return self._graph

