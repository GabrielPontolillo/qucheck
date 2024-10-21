OPENQASM 2.0;
include "qelib1.inc";
gate gate__iX q0 { x q0; }
qreg q[2];
h q[0];
cx q[0],q[1];
z q[0];
z q[0];
y q[0];
gate__iX q[1];
x q[0];
cx q[0],q[1];
h q[0];
