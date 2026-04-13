import unittest
from qiskit import QuantumCircuit
from factories.algorithm_factory import get_qft_circuit, get_iqft_circuit

class TestAlgorithmFactory(unittest.TestCase):
    def test_get_qft_circuit(self):
        n = 3
        qc = get_qft_circuit(n)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, n)
        self.assertEqual(qc.name, "QFT")
        
    def test_get_iqft_circuit(self):
        n = 3
        qc = get_iqft_circuit(n)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, n)
        self.assertEqual(qc.name, "IQFT")

    def test_get_qft_errors(self):
        with self.assertRaises(ValueError):
            get_qft_circuit(0)
        with self.assertRaises(ValueError):
            get_iqft_circuit(-1)

if __name__ == "__main__":
    unittest.main()
