OPENQASM 2.0;
include "qelib1.inc";
gate dcx q0,q1 { cx q0,q1; cx q1,q0; }
qreg q[2];
h q[0];
cx q[0],q[1];
z q[0];
x q[0];
cx q[0],q[1];
dcx q[0],q[1];
h q[0];
