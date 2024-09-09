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
            zz(PI() / 2.0, qubits[1], qubits[0]);
            zz(PI() / 4.0, qubits[2], qubits[0]);
            zz(PI() / 8.0, qubits[3], qubits[0]);
            zz(PI() / 16.0, qubits[4], qubits[0]);
            H(qubits[1]);
            zz(PI() / 2.0, qubits[2], qubits[1]);
            zz(PI() / 4.0, qubits[3], qubits[1]);
            zz(PI() / 8.0, qubits[4], qubits[1]);
            H(qubits[2]);
            zz(PI() / 2.0, qubits[3], qubits[2]);
            zz(PI() / 4.0, qubits[4], qubits[2]);
            H(qubits[3]);
            zz(PI() / 2.0, qubits[4], qubits[3]);
            H(qubits[4]);
            SWAP(qubits[0], qubits[4]);
            SWAP(qubits[1], qubits[3]);
            ResetAll(qubits);
        }
        return (c);
    }
}
