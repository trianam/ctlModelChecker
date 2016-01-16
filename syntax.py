class Syntax(object):
    """
    Simple container for all the keywords for the syntax of the
    configuration files.
    """
    
    _true         = 'true'
    _ap           = 'ap'
    _land         = '&'
    _lor          = '|'
    _lnot         = '!'
    _implies      = '->'
    _equals       = '='
    _exNext       = 'EX'
    _exUntil      = 'EU'
    _exAlways     = 'EG'
    _exEventually = 'EF'
    _faNext       = 'AX'
    _faUntil      = 'AU'
    _faAlways     = 'AG'
    _faEventually = 'AF'
    _exWeakUntil  = 'EW'
    _faWeakUntil  = 'AW'
    _phiNode      = 'phi'
    _leftSon      = '<'
    _rightSon     = '>'

    @property
    def true(self):
        return type(self)._true
    @property
    def ap(self):
        return type(self)._ap
    @property
    def land(self):
        return type(self)._land
    @property
    def lor(self):
        return type(self)._lor
    @property
    def lnot(self):
        return type(self)._lnot
    @property
    def implies(self):
        return type(self)._implies
    @property
    def equals(self):
        return type(self)._equals
    @property
    def exNext(self):
        return type(self)._exNext
    @property
    def exUntil(self):
        return type(self)._exUntil
    @property
    def exAlways(self):
        return type(self)._exAlways
    @property
    def exEventually(self):
        return type(self)._exEventually
    @property
    def faNext(self):
        return type(self)._faNext
    @property
    def faUntil(self):
        return type(self)._faUntil
    @property
    def faAlways(self):
        return type(self)._faAlways
    @property
    def faEventually(self):
        return type(self)._faEventually
    @property
    def exWeakUntil(self):
        return type(self)._exWeakUntil
    @property
    def faWeakUntil(self):
        return type(self)._faWeakUntil
    @property
    def phiNode(self):
        return type(self)._phiNode
    @property
    def leftSon(self):
        return type(self)._leftSon
    @property
    def rightSon(self):
        return type(self)._rightSon
