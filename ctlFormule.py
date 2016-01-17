import matplotlib.pyplot as plt
import networkx as nx
import syntax

class CtlFormule(object):
    """
    Class that contains the tree for a CTL formula parsed from a
    configuration file passed during costruction.
    """
    
    def __init__(self, filename):
        self._syntax = syntax.Syntax()
        self._graph = nx.DiGraph()
        
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

