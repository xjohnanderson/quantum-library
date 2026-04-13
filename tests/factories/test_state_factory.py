import unittest
import numpy as np
from qiskit.quantum_info import Statevector
from factories.state_factory import (
    get_cz_statevector,
    get_cx_statevector,
    get_cy_statevector,
    get_bv_oracle_statevector,
    _evolve_x_basis
)
from factories.basis_factory import X_BASIS

class TestStateFactory(unittest.TestCase):
    def test_get_cz_statevector(self):
        # CZ |++> is an entangled state, not in X_BASIS
        sv = get_cz_statevector('++')
        expected = Statevector([0.5, 0.5, 0.5, -0.5])
        self.assertTrue(sv.equiv(expected))
        
    def test_get_cx_statevector(self):
        # CX(0, 1) where 0 is control, 1 is target
        # X_BASIS['+-']: Q0=+, Q1=-. CX on |+-> results in |--->
        sv = get_cx_statevector('+-')
        self.assertTrue(sv.equiv(X_BASIS['--']))
        
        # X_BASIS['-+' ]: Q0=-, Q1=+. CX on |-+> results in |- +> (no change because target is +)
        sv = get_cx_statevector('-+')
        self.assertTrue(sv.equiv(X_BASIS['-+' ]))

    def test_get_cy_statevector(self):
        sv = get_cy_statevector('++')
        self.assertIsInstance(sv, Statevector)
        self.assertEqual(sv.num_qubits, 2)

    def test_get_bv_oracle_statevector(self):
        s = "11"
        sv = get_bv_oracle_statevector(s)
        self.assertEqual(sv.num_qubits, 3)
        # Expected: |-> tensor H^n |s>
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(2)
        qc.x(0)
        qc.x(1)
        qc.h([0, 1])
        expected_in = Statevector.from_instruction(qc)
        expected = Statevector.from_label('-').tensor(expected_in)
        self.assertTrue(sv.equiv(expected))

    def test_evolve_x_basis_errors(self):
        with self.assertRaises(ValueError):
            _evolve_x_basis('invalid', 'cx')
        with self.assertRaises(NotImplementedError):
            _evolve_x_basis('++', 'swap')

if __name__ == "__main__":
    unittest.main()
