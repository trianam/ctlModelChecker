import matplotlib.pyplot as plt
import networkx as nx

class Ts:
    def __init__(self, filename):
        self.graph = nx.DiGraph()
        
        f = open(filename, 'r')
        nodesPart = True
        for line in f:
            fields = line.split()
            if nodesPart and len(fields) == 0:
                nodesPart = False
                continue

            if nodesPart:
                if (len(fields) <= 2):
                    self.graph.add_node(fields[0], initial=(fields[1]=='true'), att=[])
                else:
                    self.graph.add_node(fields[0], initial=(fields[1]=='true'), att=fields[2].split(',',fields[2].count(',')))

            else:
                self.graph.add_edge(fields[0], fields[1])

    def draw(self):
        labels=dict((n,{'l':n,'d':d['att']}) for n,d in self.graph.nodes(data=True))
        nx.draw_networkx(self.graph, labels=labels)
        plt.show()
