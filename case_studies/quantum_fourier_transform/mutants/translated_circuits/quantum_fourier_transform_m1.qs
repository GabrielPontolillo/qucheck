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
            using(qubits = Qubit[1]) {
                u3(param0, param1 - PI() / 2.0, PI() / 2.0 - param1, qubits[0]);
                ResetAll(qubits);
            }
        }
}
    operation Circuit() : (Int) {
        mutable c = 0;
        using(qubits = Qubit[5]) {
            H(qubits[0]);
            H(qubits[1]);
            H(qubits[2]);
            H(qubits[3]);
            H(qubits[4]);
            r(PI() / 2.0, 1.0, qubits[0]);
            r(PI() / 2.0, 2.0, qubits[1]);
            r(PI() / 2.0, 3.0, qubits[2]);
            r(PI() / 2.0, 4.0, qubits[3]);
            r(PI() / 4.0, 2.0, qubits[0]);
            r(PI() / 4.0, 3.0, qubits[1]);
            r(PI() / 4.0, 4.0, qubits[2]);
            r(PI() / 8.0, 3.0, qubits[0]);
            r(PI() / 8.0, 4.0, qubits[1]);
            r(PI() / 16.0, 4.0, qubits[0]);
            SWAP(qubits[0], qubits[4]);
            SWAP(qubits[1], qubits[3]);
            ResetAll(qubits);
        }
        return (c);
    }
}
