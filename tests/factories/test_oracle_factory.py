import unittest
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator, Statevector
from factories.oracle_factory import (
    get_bit_flip_oracle,
    get_phase_flip_oracle,
    get_bernstein_vazirani_oracle,
    get_dj_oracle,
    create_simon_oracle
)

class TestOracleFactory(unittest.TestCase):
    def test_get_bit_flip_oracle(self):
        # Case c0: f(x) = 0
        gate = get_bit_flip_oracle('c0')
        qc = QuantumCircuit(2)
        qc.append(gate, [0, 1])
        op = Operator.from_circuit(qc)
        # Should be identity
        self.assertTrue(op.equiv(Operator.from_label('II')))
        
        # Case b0: f(x) = x
        gate = get_bit_flip_oracle('b0')
        qc = QuantumCircuit(2)
        qc.append(gate, [0, 1])
        op = Operator.from_circuit(qc)
        # Should be CX(0, 1)
        expected = QuantumCircuit(2)
        expected.cx(0, 1)
        self.assertTrue(op.equiv(Operator.from_circuit(expected)))

    def test_get_phase_flip_oracle(self):
        # 2-qubit oracle marking |11>
        gate = get_phase_flip_oracle(2, '11')
        qc = QuantumCircuit(2)
        qc.append(gate, [0, 1])
        
        # Verify it flips phase of |11>
        # |11> -> -|11>
        sv = Statevector.from_label('11').evolve(qc)
        self.assertTrue(sv.equiv(-Statevector.from_label('11')))
        
        # |01> -> |01>
        sv = Statevector.from_label('01').evolve(qc)
        self.assertTrue(sv.equiv(Statevector.from_label('01')))

    def test_get_bernstein_vazirani_oracle(self):
        s = "11"
        gate = get_bernstein_vazirani_oracle(s)
        qc = QuantumCircuit(3)
        qc.append(gate, [0, 1, 2])
        
        # f(x) = s.x
        # x=11 -> s.x = 1*1 ^ 1*1 = 0. f(11)=0. Auxiliary 2 stays same.
        sv = Statevector.from_label('011').evolve(qc)
        self.assertTrue(sv.equiv(Statevector.from_label('011')))
        
        # x=01 -> s.x = 1*0 ^ 1*1 = 1. f(01)=1. Auxiliary 2 flips.
        sv = Statevector.from_label('001').evolve(qc)
        self.assertTrue(sv.equiv(Statevector.from_label('101')))

    def test_get_dj_oracle_constant(self):
        # constant_1
        gate = get_dj_oracle(2, 'constant_1')
        qc = QuantumCircuit(3)
        qc.append(gate, [0, 1, 2])
        # Should flip auxiliary regardless of input
        sv = Statevector.from_label('000').evolve(qc)
        self.assertTrue(sv.equiv(Statevector.from_label('100')))

    def test_get_dj_oracle_balanced(self):
        gate = get_dj_oracle(2, 'balanced')
        qc = QuantumCircuit(3)
        qc.append(gate, [0, 1, 2])
        # f(x) = x0 ^ x1
        # x=01 -> f(01)=1. Flip auxiliary.
        sv = Statevector.from_label('001').evolve(qc)
        self.assertTrue(sv.equiv(Statevector.from_label('101')))
        # x=11 -> f(11)=0. auxiliary stays.
        sv = Statevector.from_label('011').evolve(qc)
        self.assertTrue(sv.equiv(Statevector.from_label('011')))

    def test_create_simon_oracle(self):
        s = "11"
        gate = create_simon_oracle(s)
        qc = QuantumCircuit(4)
        qc.append(gate, [0, 1, 2, 3])
        
        # f(x) = f(x ^ s)
        # x=00 -> f(00)
        sv00 = Statevector.from_label('0000').evolve(qc)
        # x=11 -> f(11)
        sv11 = Statevector.from_label('0011').evolve(qc)
        
      
        
        self.assertTrue(sv00.equiv(Statevector.from_label('0000')))
        self.assertTrue(sv11.equiv(Statevector.from_label('0011')))

if __name__ == "__main__":
    unittest.main()
