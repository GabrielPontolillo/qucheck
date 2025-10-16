namespace QSharpCheck {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;

    operation Teleport(q0 : Qubit, q1 : Qubit, q2 : Qubit) : Unit {
            H(q1);
            //CNOT(q1, q2);
            //Controlled SX([q1], (q2));
            //can be decomposed into ch cs ch
            Controlled H([q1], (q2));
            Controlled S([q1], (q2));
            Controlled H([q1], (q2));

            CNOT(q0, q1);
            H(q0);

            CNOT(q1, q2);
            Controlled Z([q0], (q2));
    }
}
