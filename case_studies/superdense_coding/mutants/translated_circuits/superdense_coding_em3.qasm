OPENQASM 2.0;
include "qelib1.inc";
gate iZ q0 { z q0; }
qreg q[2];
h q[0];
cx q[0],q[1];
x q[0];
y q[0];
iZ q[1];
z q[0];
x q[0];
cx q[0],q[1];
h q[0];
