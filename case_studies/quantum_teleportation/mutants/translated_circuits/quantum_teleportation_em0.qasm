OPENQASM 2.0;
include "qelib1.inc";
gate iY q0 { y q0; }
qreg q[3];
h q[1];
cx q[1],q[2];
z q[2];
x q[2];
iY q[2];
cx q[0],q[1];
h q[0];
cx q[1],q[2];
cz q[0],q[2];
