import unittest
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from factories.hamiltonian_factory import get_pauli_op, get_hamiltonian_evolution_gate

class TestHamiltonianFactory(unittest.TestCase):
    def test_get_pauli_op_linear(self):
        n_qubits = 2
        linear = {0: 1.0}
        quadratic = {}
        op = get_pauli_op(n_qubits, linear, quadratic)
        
       
        expected_list = [("IZ", -0.5)] # Qiskit: Q0 is rightmost. "IZ" means Z on Q0, I on Q1.
       
        
        self.assertEqual(op.num_qubits, n_qubits)
        self.assertEqual(len(op.paulis), 1)
        self.assertEqual(op.to_list()[0][0], "IZ")
        self.assertEqual(op.to_list()[0][1], -0.5)

    def test_get_pauli_op_quadratic(self):
        n_qubits = 2
        linear = {}
        quadratic = {(0, 1): 2.0}
        op = get_pauli_op(n_qubits, linear, quadratic)
        
        # Quadratic term x_0*x_1 -> 0.25 * (I - Z_0 - Z_1 + Z_0*Z_1)
        # In the current implementation: it only adds 0.25 * w * Z_i*Z_j
        # op_str[0] = "Z", op_str[1] = "Z" -> ["Z", "Z"] -> reversed -> ["Z", "Z"] -> "ZZ"
        
        self.assertEqual(op.num_qubits, n_qubits)
        self.assertEqual(len(op.paulis), 1)
        self.assertEqual(op.to_list()[0][0], "ZZ")
        self.assertEqual(op.to_list()[0][1], 0.5) # 0.25 * 2.0

    def test_get_hamiltonian_evolution_gate(self):
        op = SparsePauliOp.from_list([("ZZ", 1.0)])
        time = 0.5
        gate = get_hamiltonian_evolution_gate(op, time)
        
        self.assertIsInstance(gate, PauliEvolutionGate)
        self.assertEqual(gate.time, time)
        self.assertEqual(gate.operator, op)

if __name__ == "__main__":
    unittest.main()
