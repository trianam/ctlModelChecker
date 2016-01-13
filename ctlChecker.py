#import networkx as nx

class CtlChecker:
    def __init__(self, lts):
        self._callDic = {
            'true':self._satTrue,
            'ap':self._satAp,
            'and':self._satAnd,
            'not':self._satNot,
            'next':self._satNext,
            'until':self._satUntil,
            'always':self._satAlways,
        }

        self._lts = lts
        
    def _satTrue(self, phi, nodo):
        return set(self._lts.graph.nodes())

    def _satAp(self, phi, nodo):
        retSet = set()
        for stato,att in self._lts.graph.nodes(data=True):
            if phi.graph.node[nodo]['val'] in att['att']:
               retSet.add(stato)

        return retSet

    def _satAnd(self, phi, nodo):
        return self._sat(phi, phi.graph.successors(nodo)[0]).intersection(self._sat(phi, phi.graph.successors(nodo)[1]))

    def _satNot(self, phi, nodo):
        return set(self._lts.graph.nodes()).difference(self._sat(phi, phi.graph.successors(nodo)[0]))

    def _satNext(self, phi, nodo):
        retSet = set()
        satPhi = self._sat(phi, phi.graph.successors(nodo)[0])

        for stato in self._lts.graph.nodes():
            if set(self._lts.graph.successors(stato)).intersection(satPhi): #true if not empty
                retSet.add(stato)

        return retSet

    def _satUntil(self, phi, nodo):
        E = self._sat(phi, phi.graph.successors(nodo)[1])
        T = E.copy()

        while E: #while not empty
            r = E.pop()
            for s in self._lts.graph.predecessors(r):
                if s in self._sat(phi, phi.graph.successors(nodo)[0]).difference(T):
                    E.add(s)
                    T.add(s)
        return T


    def _satAlways(self, phi, nodo):
        T = self._sat(phi, phi.graph.successors(nodo)[0])
        E = set(self._lts.graph.nodes()).difference(T)
        count = dict()
        for s in T:
            count[s] = len(self._lts.graph.successors(s))

        while E:
            r = E.pop()
            for s in self._lts.graph.predecessors(r):
                if s in T:
                    count[s] = count[s]-1
                    if count[s] == 0:
                        T.remove(s)
                        E.add(s)

        return T

    def _sat(self, phi, nodo):
        if (phi.graph.node[nodo]['form'] in self._callDic.keys()) :
            return self._callDic[phi.graph.node[nodo]['form']](phi, nodo)

    def check(self, phi):
        sats = self._sat(phi, [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0])
        initials = set([s for s,a in self._lts.graph.nodes(data=True) if a['initial'] ==True])
        return initials.issubset(sats)

    def sat(self, phi):
        return (self._sat(phi, [s for s,a in phi.graph.nodes(data=True) if a['root'] ==True][0]))
