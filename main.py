#!/usr/bin/python

import ts
import formule
import ctlChecker

print('============== Test')
ts1 = ts.Ts('conf/ts1.conf')
form1 = formule.Formule('conf/form1.conf')
form2 = formule.Formule('conf/example-6.22.frm')
checker = ctlChecker.CtlChecker(ts1)
print('---a')
print(checker.check(form1))
print(checker.sat(form1))
print('---b')
print(checker.check(form2))
print(checker.sat(form2))

print('============== Oven')
tsOven = ts.Ts('conf/oven.cfg')
formOven = formule.Formule('conf/formOven1.cfg')
checkOven = ctlChecker.CtlChecker(tsOven)
print(checkOven.sat(formOven))

print('============= Morgagni')
tsMorgagni = ts.Ts('conf/tsMorgagni.cfg')
forMorgagni = formule.Formule('conf/forMorgagni.cfg')
checkMorgagni = ctlChecker.CtlChecker(tsMorgagni)
print(checkMorgagni.check(forMorgagni))

print('============= Morgagni2')
tsMorgagni2 = ts.Ts('conf/morgagni2.ts')
forMorgagni2 = formule.Formule('conf/morgagni2-1.frm')
checkMorgagni2 = ctlChecker.CtlChecker(tsMorgagni2)
print(checkMorgagni2.check(forMorgagni2))


print('============== BOOK 6.4')
tsBook6_4 = ts.Ts('conf/book6.4.ts')
checkBook6_4 = ctlChecker.CtlChecker(tsBook6_4)

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
