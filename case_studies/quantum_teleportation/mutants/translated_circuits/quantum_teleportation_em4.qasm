OPENQASM 2.0;
include "qelib1.inc";
gate gate__iX q0 { x q0; }
qreg q[3];
h q[1];
cx q[1],q[2];
cx q[0],q[1];
z q[2];
y q[2];
gate__iX q[2];
h q[0];
cx q[1],q[2];
cz q[0],q[2];
