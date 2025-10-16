namespace QSharpCheck {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;


    operation Superdense_coding(b1: Bool, b2: Bool) : (Bool, Bool) {
        using(qubits = Qubit[2]) {
            Z(qubits[0]);
            X(qubits[0]);
            Ry(-PI(), qubits[0]);

            H(qubits[0]);
            CNOT(qubits[0], qubits[1]);

            if (b1==true){
                Z(qubits[0]);
            }

            if (b2==true){
                X(qubits[0]);
            }

            CNOT(qubits[0], qubits[1]);
            H(qubits[0]);
            return (MResetZ(qubits[0]) == One, MResetZ(qubits[1]) == One);
        }
    }
}
