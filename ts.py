import matplotlib.pyplot as plt
import networkx as nx
import syntax

class Ts:
    def __init__(self, filename):
        self._syntax = syntax.Syntax()        
        self.graph = nx.DiGraph()
        
        f = open(filename, 'r')
        nodesPart = True
        for line in f:
            fields = line.split('//')[0].split()
            if nodesPart and len(fields) == 0:
                nodesPart = False
                continue

            if nodesPart:
                if (len(fields) <= 2):
                    self.graph.add_node(fields[0], initial=(fields[1]==self._syntax.true), att=[])
                else:
                    self.graph.add_node(fields[0], initial=(fields[1]==self._syntax.true), att=fields[2].split(',',fields[2].count(',')))

            else:
                self.graph.add_edge(fields[0], fields[1])

    def draw(self):
        labels=dict((n,{'l':n,'d':d['att']}) for n,d in self.graph.nodes(data=True))
        nx.draw_networkx(self.graph, labels=labels)
        plt.show()
