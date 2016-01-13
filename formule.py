import matplotlib.pyplot as plt
import networkx as nx

class Formule:
    def __init__(self, filename):
        self.graph = nx.DiGraph()
        
        f = open(filename, 'r')
        nodesPart = True
        firstLine = True
        for line in f:
            fields = line.split('//')[0].split()
            if nodesPart and len(fields) == 0:
                nodesPart = False
                continue

            if nodesPart:
                if (fields[1] == 'ap'):
                    self.graph.add_node(fields[0], root=firstLine, form=fields[1], val=fields[2])
                else:
                    self.graph.add_node(fields[0], root=firstLine, form=fields[1])
                firstLine = False

            else:
                self.graph.add_edge(fields[0], fields[1])

    def draw(self):
        labels=dict((n,{'l':n,'d':d['form']}) for n,d in self.graph.nodes(data=True))
        nx.draw_networkx(self.graph, labels=labels)
        plt.show()
