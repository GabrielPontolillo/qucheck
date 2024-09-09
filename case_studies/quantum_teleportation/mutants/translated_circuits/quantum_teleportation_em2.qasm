OPENQASM 2.0;
include "qelib1.inc";
gate iX q0 { x q0; }
qreg q[3];
h q[1];
y q[0];
z q[0];
iX q[0];
cx q[1],q[2];
cx q[0],q[1];
h q[0];
cx q[1],q[2];
cz q[0],q[2];
