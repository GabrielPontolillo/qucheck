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
    
    operation Circuit() : (Int) {
        mutable c = 0;
        using(qubits = Qubit[5]) {
            H(qubits[0]);
            Z(qubits[0]);
            S(qubits[0]);
            S(qubits[0]);
            cu1([qubits[1]], (PI() / 2.0, qubits[0]));
            Z(qubits[0]);
            S(qubits[0]);
            S(qubits[0]);
            cu1([qubits[2]], (PI() / 4.0, qubits[0]));
            Z(qubits[0]);
            S(qubits[0]);
            S(qubits[0]);
            cu1([qubits[3]], (PI() / 8.0, qubits[0]));
            Z(qubits[0]);
            S(qubits[0]);
            S(qubits[0]);
            cu1([qubits[4]], (PI() / 16.0, qubits[0]));
            Z(qubits[0]);
            H(qubits[1]);
            S(qubits[0]);
            cu1([qubits[2]], (PI() / 2.0, qubits[1]));
            S(qubits[0]);
            cu1([qubits[3]], (PI() / 4.0, qubits[1]));
            Z(qubits[0]);
            cu1([qubits[4]], (PI() / 8.0, qubits[1]));
            S(qubits[0]);
            H(qubits[2]);
            S(qubits[0]);
            cu1([qubits[3]], (PI() / 2.0, qubits[2]));
            Z(qubits[0]);
            cu1([qubits[4]], (PI() / 4.0, qubits[2]));
            S(qubits[0]);
            H(qubits[3]);
            S(qubits[0]);
            cu1([qubits[4]], (PI() / 2.0, qubits[3]));
            Z(qubits[0]);
            H(qubits[4]);
            S(qubits[0]);
            S(qubits[0]);
            Z(qubits[0]);
            S(qubits[0]);
            S(qubits[0]);
            Z(qubits[0]);
            S(qubits[0]);
            S(qubits[0]);
            SWAP(qubits[0], qubits[4]);
            SWAP(qubits[1], qubits[3]);
            ResetAll(qubits);
        }
        return (c);
    }
}
