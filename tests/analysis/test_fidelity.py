import unittest
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix
from analysis.fidelity import (
    is_pure_state,
    compute_fidelity,
    compute_trace_distance,
    create_mixed_state,
)


class TestFidelity(unittest.TestCase):
    def setUp(self):
        self.plus = Statevector.from_label("+")
        self.minus = Statevector.from_label("-")
        self.zero = Statevector.from_label("0")
        self.one = Statevector.from_label("1")

    def test_is_pure_state(self):
        # Statevector is always pure
        self.assertTrue(is_pure_state(self.plus))

        # DensityMatrix from Statevector is pure
        rho_plus = DensityMatrix(self.plus)
        self.assertTrue(is_pure_state(rho_plus))

        # Mixed state is not pure
        rho_mixed = 0.5 * (DensityMatrix(self.zero).data + DensityMatrix(self.one).data)
        self.assertFalse(is_pure_state(rho_mixed))

        # Numpy array (pure)
        self.assertTrue(is_pure_state(self.zero.data))

    def test_compute_fidelity(self):
        # Same state: F = 1
        self.assertAlmostEqual(compute_fidelity(self.plus, self.plus), 1.0)

        # Orthogonal states: F = 0
        self.assertAlmostEqual(compute_fidelity(self.zero, self.one), 0.0)

        # Non-orthogonal pure states: |<0|+>|^2 = 0.5
        self.assertAlmostEqual(compute_fidelity(self.zero, self.plus), 0.5)

        # Mixed state fidelity
        # rho = 0.5|0><0| + 0.5|1><1| = I/2
        # F(|0>, I/2) = <0|I/2|0> = 0.5
        rho_mixed = create_mixed_state([self.zero, self.one], [0.5, 0.5])
        self.assertAlmostEqual(compute_fidelity(self.zero, rho_mixed), 0.5)

    def test_compute_trace_distance(self):
        # Same state: D = 0
        self.assertAlmostEqual(compute_trace_distance(self.plus, self.plus), 0.0)

        # Orthogonal states: D = 1
        self.assertAlmostEqual(compute_trace_distance(self.zero, self.one), 1.0)

        # |0> and |+>: D = 1/2 || |0><0| - |+><+| ||_1
        # |0><0| = [[1, 0], [0, 0]]
        # |+><+| = [[0.5, 0.5], [0.5, 0.5]]
        # diff = [[0.5, -0.5], [-0.5, -0.5]]
        # eigenvalues of diff: +/- 1/sqrt(2)
        # Trace distance = 0.5 * (1/sqrt(2) + 1/sqrt(2)) = 1/sqrt(2)
        self.assertAlmostEqual(compute_trace_distance(self.zero, self.plus), 1 / np.sqrt(2))

    def test_create_mixed_state(self):
        # Valid mixture
        rho = create_mixed_state([self.zero, self.one], [0.3, 0.7])
        self.assertIsInstance(rho, DensityMatrix)
        expected = 0.3 * DensityMatrix(self.zero).data + 0.7 * DensityMatrix(self.one).data
        np.testing.assert_array_almost_equal(rho.data, expected)

        # Invalid lengths
        with self.assertRaises(ValueError):
            create_mixed_state([self.zero], [0.5, 0.5])

        # Probabilities don't sum to 1
        with self.assertRaises(ValueError):
            create_mixed_state([self.zero, self.one], [0.5, 0.6])


if __name__ == "__main__":
    unittest.main()
