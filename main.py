#!/usr/bin/python

import lts
import formule
import ctlChecker

lts1 = lts.Lts('conf/lts1.conf')
form1 = formule.Formule('conf/form1.conf')
checker = ctlChecker.CtlChecker(lts1)
print(checker.check(form1))
print(checker.sat(form1))

print('==============')
ltsOven = lts.Lts('conf/oven.cfg')
formOven = formule.Formule('conf/formOven1.cfg')
checkOven = ctlChecker.CtlChecker(ltsOven)
print(checkOven.sat(formOven))

print('=============')
ltsMorgagni = lts.Lts('conf/ltsMorgagni.cfg')
forMorgagni = formule.Formule('conf/forMorgagni.cfg')
checkMorgagni = ctlChecker.CtlChecker(ltsMorgagni)
print(checkMorgagni.check(forMorgagni))


print('============== BOOK 6.4')
ltsBook6_4 = lts.Lts('conf/book6.4.lts')
checkBook6_4 = ctlChecker.CtlChecker(ltsBook6_4)

forBook6_4_1 = formule.Formule('conf/book6.4-1.frm')
forBook6_4_2 = formule.Formule('conf/book6.4-2.frm')
forBook6_4_3 = formule.Formule('conf/book6.4-3.frm')
forBook6_4_4 = formule.Formule('conf/book6.4-4.frm')
forBook6_4_5 = formule.Formule('conf/book6.4-5.frm')
forBook6_4_6 = formule.Formule('conf/book6.4-6.frm')

print('1: {}'.format(checkBook6_4.sat(forBook6_4_1)))
print('2: {}'.format(checkBook6_4.sat(forBook6_4_2)))
print('3: {}'.format(checkBook6_4.sat(forBook6_4_3)))
print('4: {}'.format(checkBook6_4.sat(forBook6_4_4)))
print('5: {}'.format(checkBook6_4.sat(forBook6_4_5)))
print('6: {}'.format(checkBook6_4.sat(forBook6_4_6)))
