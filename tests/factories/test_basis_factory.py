import unittest
import numpy as np
from qiskit.quantum_info import Statevector
from factories.basis_factory import (
    get_w_state,
    get_2qubit_z_basis,
    get_2qubit_x_basis,
    get_2qubit_y_basis,
    get_bell_basis,
    get_3qubit_z_basis,
    get_ghz_basis,
    Z_BASIS,
    X_BASIS,
    Y_BASIS,
    BELL_BASIS,
    GHZ_BASIS
)

class TestBasisFactory(unittest.TestCase):
    def test_get_w_state(self):
        w_state = get_w_state()
        self.assertIsInstance(w_state, Statevector)
        self.assertEqual(w_state.dim, 8)
        # Expected state: (|001> + |010> + |100>) / sqrt(3)
        # In Qiskit's little-endian ordering:
        # |001> is index 1
        # |010> is index 2
        # |100> is index 4
        expected_data = np.zeros(8, dtype=complex)
        expected_data[1] = 1/np.sqrt(3)
        expected_data[2] = 1/np.sqrt(3)
        expected_data[4] = 1/np.sqrt(3)
        np.testing.assert_array_almost_equal(w_state.data, expected_data)

    def test_get_2qubit_z_basis(self):
        z_basis = get_2qubit_z_basis()
        self.assertEqual(len(z_basis), 4)
        for label, sv in z_basis.items():
            self.assertIsInstance(sv, Statevector)
            self.assertEqual(sv.dim, 4)
            self.assertEqual(sv, Statevector.from_label(label))

    def test_get_2qubit_x_basis(self):
        x_basis = get_2qubit_x_basis()
        self.assertEqual(len(x_basis), 4)
        expected_labels = ['++', '+-', '-+', '--']
        self.assertCountEqual(x_basis.keys(), expected_labels)
        for label, sv in x_basis.items():
            self.assertIsInstance(sv, Statevector)
            # In Qiskit, '+' is (|0> + |1>)/sqrt(2), '-' is (|0> - |1>)/sqrt(2)
            # The function uses tensor product: map_states[label[1]] ^ map_states[label[0]]
            # This is correct for Qiskit's tensor product order.
            
            # Verify orthogonality
            for other_label, other_sv in x_basis.items():
                if label == other_label:
                    self.assertAlmostEqual(sv.inner(other_sv), 1.0)
                else:
                    self.assertAlmostEqual(sv.inner(other_sv), 0.0)

    def test_get_2qubit_y_basis(self):
        y_basis = get_2qubit_y_basis()
        self.assertEqual(len(y_basis), 4)
        expected_labels = ['rr', 'rl', 'lr', 'll']
        self.assertCountEqual(y_basis.keys(), expected_labels)
        for label, sv in y_basis.items():
            self.assertIsInstance(sv, Statevector)
            # Verify orthogonality
            for other_label, other_sv in y_basis.items():
                if label == other_label:
                    self.assertAlmostEqual(sv.inner(other_sv), 1.0)
                else:
                    self.assertAlmostEqual(sv.inner(other_sv), 0.0)

    def test_get_bell_basis(self):
        bell_basis = get_bell_basis()
        self.assertEqual(len(bell_basis), 4)
        expected_labels = ['phi+', 'phi-', 'psi+', 'psi-']
        self.assertCountEqual(bell_basis.keys(), expected_labels)
        for label, sv in bell_basis.items():
            self.assertIsInstance(sv, Statevector)
            # Verify orthogonality
            for other_label, other_sv in bell_basis.items():
                if label == other_label:
                    self.assertAlmostEqual(sv.inner(other_sv), 1.0)
                else:
                    self.assertAlmostEqual(sv.inner(other_sv), 0.0)

    def test_get_3qubit_z_basis(self):
        z_basis = get_3qubit_z_basis()
        self.assertEqual(len(z_basis), 8)
        for label, sv in z_basis.items():
            self.assertIsInstance(sv, Statevector)
            self.assertEqual(sv.dim, 8)
            self.assertEqual(sv, Statevector.from_label(label))

    def test_get_ghz_basis(self):
        ghz_basis = get_ghz_basis()
        self.assertEqual(len(ghz_basis), 8)
        # Check standard GHZ
        expected_ghz_plus = (Statevector.from_label('000') + Statevector.from_label('111')) / np.sqrt(2)
        self.assertEqual(ghz_basis['ghz+'], expected_ghz_plus)
        
        for label, sv in ghz_basis.items():
            self.assertIsInstance(sv, Statevector)
            # Verify orthogonality
            for other_label, other_sv in ghz_basis.items():
                if label == other_label:
                    self.assertAlmostEqual(sv.inner(other_sv), 1.0)
                else:
                    self.assertAlmostEqual(sv.inner(other_sv), 0.0)

    def test_constants(self):
        self.assertEqual(len(Z_BASIS), 4)
        self.assertEqual(len(X_BASIS), 4)
        self.assertEqual(len(Y_BASIS), 4)
        self.assertEqual(len(BELL_BASIS), 4)
        self.assertEqual(len(GHZ_BASIS), 8)

if __name__ == '__main__':
    unittest.main()
