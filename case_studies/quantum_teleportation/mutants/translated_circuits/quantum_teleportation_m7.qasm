OPENQASM 2.0;
include "qelib1.inc";
gate iswap q0,q1 { s q0; s q1; h q0; cx q0,q1; cx q1,q0; h q1; }
qreg q[3];
h q[1];
cx q[1],q[2];
cx q[0],q[1];
h q[0];
cx q[1],q[2];
iswap q[0],q[2];
