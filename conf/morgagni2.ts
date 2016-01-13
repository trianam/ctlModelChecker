r0 true sr //sem rosso e nessuno si è accodato
r1 false sr,pc //sem rosso si sono accodati pedoni
r2 false sr,mc //sem rosso si sono accodate macchine
r3 false sr,pc,mc //sem rosso si sono accodati pedoni e macchine
s0 false sv //sem verde non è passato ne accodato nessuno
s1 false sv,pv //sem verde sono passati pedoni, nessuno rimasto in coda
s2 false sv,mv //sem verde sono passate macchine, nessuno rimasto in coda
s3 false sv,pv,mv //sem verde sono passati pedoni e macchine, nessuno rimasto in coda
s4 false sv,pv,pc //sem verde sono passati pedoni, pedoni rimasti in coda
s5 false sv,pv,mc //sem verde sono passati pedoni, macchine rimaste in coda
s6 false sv,pv,pc,mc //sem verde sono passati pedoni, pedoni e macchine rimasti in coda
s7 false sv,pv,mv,pc //sem verde sono passati pedoni e macchine, pedoni rimasti in coda
s8 false sv,pv,mv,mc //sem verde sono passati pedoni e macchine, macchine rimaste in coda
s9 false sv,pv,mv,pc,mc //sem verde sono passati pedoni e macchine, pedoni e macchine rimasti in coda
s10 false sv,mv,mc //sem verde sono passate macchine, macchine rimaste in coda (sv,mv,pc e sv,mv,mc,pc non possibili)

r0 s0
r0 s1
r0 s2
r0 s3
r0 s4
r0 s5
r0 s6
r0 s7
r0 s8
r0 s9
r0 s10
r1 s1
r1 s3
r1 s4
r1 s5
r1 s6
r1 s7
r1 s8
r1 s9
r2 s2
r2 s3
r2 s5
r2 s6
r2 s7
r2 s8
r2 s9
r2 s10
r3 s3
r3 s5
r3 s6
r3 s7
r3 s8
r3 s9
s0 r0
s0 r1
s0 r2
s0 r3
s1 r0
s1 r1
s1 r2
s1 r3
s2 r0
s2 r1
s2 r2
s2 r3
s3 r0
s3 r1
s3 r2
s3 r3
s4 r1
s4 r3
s5 r2
s5 r3
s6 r3
s7 r1
s7 r3
s8 r2
s8 r3
s9 r3
s10 r2
s10 r3
