import matplotlib.pyplot as plt
import networkx as nx

class Lts:
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
                if (fields[1] == 'NULL'):
                    self.graph.add_node(fields[0], att=[], initial=(fields[2]=='true'))
                else:
                    self.graph.add_node(fields[0], att=fields[1].split(',',fields[1].count(',')), initial=(fields[2]=='true'))

            else:
                self.graph.add_edge(fields[0], fields[1])

    def draw(self):
        labels=dict((n,{'l':n,'d':d['att']}) for n,d in self.graph.nodes(data=True))
        nx.draw_networkx(self.graph, labels=labels)
        plt.show()
