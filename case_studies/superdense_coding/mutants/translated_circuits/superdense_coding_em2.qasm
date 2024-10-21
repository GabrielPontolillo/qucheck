OPENQASM 2.0;
include "qelib1.inc";
gate gate__iZ q0 { z q0; }
qreg q[2];
h q[0];
cx q[0],q[1];
z q[0];
y q[0];
x q[0];
gate__iZ q[0];
x q[0];
cx q[0],q[1];
h q[0];
