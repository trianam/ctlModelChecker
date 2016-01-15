s0 true
s1 false start,err|
s2 false close
s3 false close,heat
s4 false start,close,err|
s5 false start,close
s6 false start,close,heat

s0 s1
s0 s2
s1 s4
s2 s0
s2 s5
s3 s3
s3 s0
s3 s2
s4 s1
s4 s2
s5 s6
s6 s3
