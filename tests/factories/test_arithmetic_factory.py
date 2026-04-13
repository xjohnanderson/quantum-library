import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit.quantum_info import Operator, Statevector
from factories.arithmetic_factory import (
    get_rfa_gate,
    n_bit_adder,
    get_modular_multiplier_gate,
    get_modular_exponentiation_circuit_matrix,
    get_modular_multiplier_circuit,
    get_modular_exponentiation_circuit_adder
)

class TestArithmeticFactory(unittest.TestCase):
    def test_get_rfa_gate(self):
        gate = get_rfa_gate()
        self.assertIsInstance(gate, Gate)
        self.assertEqual(gate.num_qubits, 5)
        self.assertEqual(gate.label, 'RFA')
        
    def test_n_bit_adder(self):
        n = 2
        qc = n_bit_adder(n)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.name, f'Adder_{n}bit')
        # qa(n) + qb(n) + qcin_out(n+1) + qsum(n) + q_ancilla(1)
        # 2 + 2 + 3 + 2 + 1 = 10 qubits
        self.assertEqual(qc.num_qubits, 10)

    def test_get_modular_multiplier_gate(self):
        # a=3, N=5. x=1 -> 3, x=2 -> 1, x=3 -> 4, x=4 -> 2, x=0 -> 0
        a, N = 3, 5
        gate = get_modular_multiplier_gate(a, N)
        self.assertEqual(gate.num_qubits, 3) # ceil(log2(5)) = 3
        
        op = Operator(gate)
        # Test applying it to |1>
        sv = Statevector.from_label('001').evolve(op)
        self.assertTrue(sv.equiv(Statevector.from_label('011'))) # |3>
        
        # Test applying it to |2>
        sv = Statevector.from_label('010').evolve(op)
        self.assertTrue(sv.equiv(Statevector.from_label('001'))) # |1>

    def test_get_modular_exponentiation_circuit_matrix(self):
        x, N, n_count = 2, 3, 2
        qc = get_modular_exponentiation_circuit_matrix(x, N, n_count)
        self.assertEqual(qc.num_qubits, n_count + 2) # n_count + ceil(log2(3))

    def test_get_modular_multiplier_circuit(self):
        a, N = 2, 3
        qc = get_modular_multiplier_circuit(a, N)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertGreater(qc.num_qubits, 0)

    def test_get_modular_exponentiation_circuit_adder(self):
        x, N, n_count = 2, 3, 2
        qc = get_modular_exponentiation_circuit_adder(x, N, n_count)
        self.assertIsInstance(qc, QuantumCircuit)

if __name__ == "__main__":
    unittest.main()
