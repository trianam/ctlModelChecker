import matplotlib.pyplot as plt
import networkx as nx
import syntax

class TransitionSystem:
    """
    Class that contains the graph for a transition system parsed from
    a configuration file passed during costruction.
    """
    
    def __init__(self, filename):
        self._syntax = syntax.Syntax()        
        self._graph = nx.DiGraph()
        
        f = open(filename, 'r')
        nodesPart = True
        for line in f:
            fields = line.split('//')[0].split()
            if nodesPart and len(fields) == 0:
                nodesPart = False
                continue

            if nodesPart:
                if (len(fields) <= 2):
                    self._graph.add_node(fields[0], initial=(fields[1]==self._syntax.true), att=[])
                else:
                    self._graph.add_node(fields[0], initial=(fields[1]==self._syntax.true), att=fields[2].split(',',fields[2].count(',')))

            else:
                self._graph.add_edge(fields[0], fields[1])

    def draw(self):
        labels=dict((n,{'l':n,'d':d['att']}) for n,d in self._graph.nodes(data=True))
        nx.draw_networkx(self._graph, labels=labels)
        plt.show()

    @property
    def graph(self):
        return self._graph

