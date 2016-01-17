#!/usr/bin/python

import transitionSystem as ts
import ctlFormule as frm
import ctlChecker as mc

print('============== Test')
ts1 = ts.TransitionSystem('conf/book6.11.ts')
form1 = frm.CtlFormule('conf/book6.12-enf.frm')
form2 = frm.CtlFormule('conf/example-6.22.frm')
form3 = frm.CtlFormule('conf/book6.11.frm')
checker = mc.CtlChecker(ts1)
print('---a')
print(checker.check(form1))
print(checker.sat(form1))
print('---b')
print(checker.check(form2))
print(checker.sat(form2))
print('---c')
print(checker.check(form3))
print(checker.sat(form3))

print('============== Oven')
tsOven = ts.TransitionSystem('conf/oven.ts')
formOven = frm.CtlFormule('conf/oven1.frm')
checkOven = mc.CtlChecker(tsOven)
print(checkOven.sat(formOven))

print('============= Morgagni')
tsMorgagni = ts.TransitionSystem('conf/morgagni.ts')
forMorgagni = frm.CtlFormule('conf/morgagni.frm')
checkMorgagni = mc.CtlChecker(tsMorgagni)
print(checkMorgagni.check(forMorgagni))

print('============= Morgagni2')
tsMorgagni2 = ts.TransitionSystem('conf/morgagni2.ts')
checkMorgagni2 = mc.CtlChecker(tsMorgagni2)

forMorgagni2_1 = frm.CtlFormule('conf/morgagni2-1.frm')
forMorgagni2_2 = frm.CtlFormule('conf/morgagni2-2.frm')
forMorgagni2_3 = frm.CtlFormule('conf/morgagni2-3.frm')
forMorgagni2_4 = frm.CtlFormule('conf/morgagni2-4.frm')

print(checkMorgagni2.check(forMorgagni2_1))
print(checkMorgagni2.check(forMorgagni2_2))
print(checkMorgagni2.check(forMorgagni2_3))
print(checkMorgagni2.check(forMorgagni2_4))


print('============== BOOK 6.4')
tsBook6_4 = ts.TransitionSystem('conf/book6.4.ts')
checkBook6_4 = mc.CtlChecker(tsBook6_4)

forBook6_4_1 = frm.CtlFormule('conf/book6.4-1.frm')
forBook6_4_2 = frm.CtlFormule('conf/book6.4-2.frm')
forBook6_4_3 = frm.CtlFormule('conf/book6.4-3.frm')
forBook6_4_3_enf = frm.CtlFormule('conf/book6.4-3-enf.frm')
forBook6_4_4 = frm.CtlFormule('conf/book6.4-4.frm')
forBook6_4_4_enf = frm.CtlFormule('conf/book6.4-4-enf.frm')
forBook6_4_5 = frm.CtlFormule('conf/book6.4-5.frm')
forBook6_4_5_enf = frm.CtlFormule('conf/book6.4-5-enf.frm')
forBook6_4_6 = frm.CtlFormule('conf/book6.4-6.frm')
forBook6_4_6_enf = frm.CtlFormule('conf/book6.4-6-enf.frm')
forBook6_4_7 = frm.CtlFormule('conf/book6.4-7.frm')

print('1    : {}'.format(checkBook6_4.sat(forBook6_4_1)))
print('2    : {}'.format(checkBook6_4.sat(forBook6_4_2)))
print('3    : {}'.format(checkBook6_4.sat(forBook6_4_3)))
print('3-enf: {}'.format(checkBook6_4.sat(forBook6_4_3_enf)))
print('4    : {}'.format(checkBook6_4.sat(forBook6_4_4)))
print('4-enf: {}'.format(checkBook6_4.sat(forBook6_4_4_enf)))
print('5    : {}'.format(checkBook6_4.sat(forBook6_4_5)))
print('5-enf: {}'.format(checkBook6_4.sat(forBook6_4_5_enf)))
print('6    : {}'.format(checkBook6_4.sat(forBook6_4_6)))
print('6-enf: {}'.format(checkBook6_4.sat(forBook6_4_6_enf)))
print('7    : {}'.format(checkBook6_4.sat(forBook6_4_7)))
