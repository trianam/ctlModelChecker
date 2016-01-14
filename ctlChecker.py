#import networkx as nx

class CtlChecker:
    def __init__(self, ts):
        self._callDic = {
            'true':self._satTrue,
            'ap':self._satAp,
            'and':self._satAnd,
            'not':self._satNot,
            'existsNext':self._satExNext,
            'existsUntil':self._satExUntil,
            'existsAlways':self._satExAlways,
            'existsEventually':self._satExEventually,
            'forallNext':self._satFaNext,
            'forallUntil':self._satFaUntil,
            'forallAlways':self._satFaAlways,
            'forallEventually':self._satFaEventually,
        }

        self._ts = ts
        
    def _satTrue(self, phi, root):
        return set(self._ts.graph.nodes())

    def _satAp(self, phi, root):
        retSet = set()
        for stato,att in self._ts.graph.nodes(data=True):
            if phi.graph.node[root]['val'] in att['att']:
               retSet.add(stato)

        return retSet

    def _satAnd(self, phi, root):
        return self._sat(phi, phi.graph.successors(root)[0]).intersection(self._sat(phi, phi.graph.successors(root)[1]))

    def _satNot(self, phi, root):
        return set(self._ts.graph.nodes()).difference(self._sat(phi, phi.graph.successors(root)[0]))

    def _satExNext(self, phi, root):
        retSet = set()
        satPhi = self._sat(phi, phi.graph.successors(root)[0])

        for stato in self._ts.graph.nodes():
            if set(self._ts.graph.successors(stato)).intersection(satPhi): #true if not empty
                retSet.add(stato)

        return retSet

    def _satExUntil(self, phi, root):
        leftSon = [x for x in phi.graph[root] if phi.graph[root][x]['son'] == 'sx'][0]
        rightSon = [x for x in phi.graph[root] if phi.graph[root][x]['son'] == 'dx'][0]
        
        E = self._sat(phi, rightSon)
        T = E.copy()

        while E: #while not empty
            r = E.pop()
            for s in self._ts.graph.predecessors(r):
                if s in self._sat(phi, leftSon).difference(T):
                    E.add(s)
                    T.add(s)
        return T


    def _satExAlways(self, phi, root):
        T = self._sat(phi, phi.graph.successors(root)[0])
        E = set(self._ts.graph.nodes()).difference(T)
        count = dict()
        for s in T:
            count[s] = len(self._ts.graph.successors(s))

        while E:
            r = E.pop()
            for s in self._ts.graph.predecessors(r):
                if s in T:
                    count[s] = count[s]-1
                    if count[s] == 0:
                        T.remove(s)
                        E.add(s)

        return T

    def _satExEventually(self, phi, root):
        return

    def _satFaNext(self, phi, root):
        return

    def _satFaUntil(self, phi, root):
        return

    def _satFaAlways(self, phi, root):
        return

    def _satFaEventually(self, phi, root):
        return

    def _sat(self, phi, root):
        if (phi.graph.node[root]['form'] in self._callDic.keys()) :
            return self._callDic[phi.graph.node[root]['form']](phi, root)

    def check(self, phi):
        sats = self._sat(phi, [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0])
        initials = set([s for s,a in self._ts.graph.nodes(data=True) if a['initial'] ==True])
        return initials.issubset(sats)

    def sat(self, phi):
        return (self._sat(phi, [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0]))
