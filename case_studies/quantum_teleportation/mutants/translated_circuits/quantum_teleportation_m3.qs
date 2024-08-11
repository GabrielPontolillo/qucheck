namespace Quantum {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;

    function SetBitValue(reg: Int, bit: Int, value: Bool): Int {
        if(value) {
            return reg ||| (1 <<< bit);
        } else {
            return reg &&& ~~~(1 <<< bit);
        }
    }
    
    operation Circuit() : Unit {
        using(qubits = Qubit[3]) {
            H(qubits[1]);
            CNOT(qubits[1], qubits[2]);
            Controlled Z([qubits[1]], (qubits[2]));
            CNOT(qubits[0], qubits[1]);
            H(qubits[0]);
            CNOT(qubits[1], qubits[2]);
            Controlled Z([qubits[0]], (qubits[2]));
            ResetAll(qubits);
        }
    }
}
