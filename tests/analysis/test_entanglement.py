import unittest
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix
from analysis.entanglement import (
    state_purity,
    verify_entanglement,
    helstrom_bound,
    compute_concurrence,
    is_entangled
)

class TestEntanglement(unittest.TestCase):
    def test_state_purity(self):
        # Pure state
        psi = Statevector.from_label('0')
        self.assertAlmostEqual(state_purity(psi), 1.0)
        
        # Mixed state: I/2
        rho = DensityMatrix(np.eye(2) / 2)
        self.assertAlmostEqual(state_purity(rho), 0.5)

    def test_verify_entanglement_separable(self):
        # Separable state |00>
        psi = Statevector.from_label('00')
        entangled, purity = verify_entanglement(psi)
        self.assertFalse(entangled)
        self.assertAlmostEqual(purity, 1.0)

        # Separable state |++>
        psi = Statevector.from_label('++')
        entangled, purity = verify_entanglement(psi)
        self.assertFalse(entangled)
        self.assertAlmostEqual(purity, 1.0)

    def test_verify_entanglement_bell(self):
        # Bell state |Phi+> = (|00> + |11>)/sqrt(2)
        psi = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
        entangled, purity = verify_entanglement(psi)
        self.assertTrue(entangled)
        self.assertAlmostEqual(purity, 0.5) # reduced state is I/2

    def test_is_entangled_convenience(self):
        # Bell state
        psi = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
        self.assertTrue(is_entangled(psi))
        
        # Separable
        self.assertFalse(is_entangled(Statevector.from_label('01')))

    def test_helstrom_bound_orthogonal(self):
        psi0 = Statevector.from_label('0')
        psi1 = Statevector.from_label('1')
        success, error = helstrom_bound(psi0, psi1)
        self.assertAlmostEqual(success, 1.0)
        self.assertAlmostEqual(error, 0.0)

    def test_helstrom_bound_non_orthogonal(self):
        psi0 = Statevector.from_label('0')
        psip = Statevector.from_label('+')
        # D = 1/sqrt(2)
        # Success = (1 + 1/sqrt(2))/2 = 0.5 + 0.3535 = 0.85355...
        success, error = helstrom_bound(psi0, psip)
        expected_success = (1 + 1/np.sqrt(2)) / 2
        self.assertAlmostEqual(success, expected_success)
        self.assertAlmostEqual(error, 1 - expected_success)

    def test_compute_concurrence(self):
        # Bell state: C=1
        phi_plus = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
        self.assertAlmostEqual(compute_concurrence(phi_plus), 1.0)
        
        # Separable state: C=0
        self.assertAlmostEqual(compute_concurrence(Statevector.from_label('01')), 0.0)
        
        # Partially entangled state?
        # Maybe cos(theta)|00> + sin(theta)|11>? C = |sin(2*theta)|
        # theta = pi/8: C = sin(pi/4) = 1/sqrt(2)
        theta = np.pi / 8
        psi = np.cos(theta) * Statevector.from_label('00') + np.sin(theta) * Statevector.from_label('11')
        self.assertAlmostEqual(compute_concurrence(psi), np.sin(2*theta))

    def test_concurrence_invalid_dim(self):
        # Single qubit
        with self.assertRaises(ValueError):
            compute_concurrence(Statevector.from_label('0'))

if __name__ == "__main__":
    unittest.main()
