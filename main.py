#!/usr/bin/python

import lts
import formule
import ctlChecker

lts1 = lts.Lts('lts1.conf')
form1 = formule.Formule('form1.conf')
checker = ctlChecker.CtlChecker(lts1)
print(checker.check(form1))

