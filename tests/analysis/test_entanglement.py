import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix
from analysis.entanglement import (
    state_purity,
    verify_entanglement,
    helstrom_bound,
    compute_concurrence,
    is_entangled
)
from analysis.fidelity import compute_fidelity, compute_trace_distance
from factories.primitive_factory import attach_bell_state_prep

class TestEntanglement(unittest.TestCase):
    def test_state_purity(self):
        # Pure state
        psi = Statevector.from_label('0')
        self.assertAlmostEqual(state_purity(psi), 1.0)
        
        # Mixed state: I/2
        rho = DensityMatrix(np.eye(2) / 2)
        self.assertAlmostEqual(state_purity(rho), 0.5)

    def test_state_purity_ndarray(self):
        # 1D array (Statevector)
        psi = np.array([1, 0])
        self.assertAlmostEqual(state_purity(psi), 1.0)
        # 2D array (DensityMatrix)
        rho = np.array([[0.5, 0], [0, 0.5]])
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
        self.assertAlmostEqual(purity, 0.5)

    def test_verify_entanglement_mixed_separable(self):
        # Maximally mixed state I/4 is separable.
        rho = DensityMatrix(np.eye(4) / 4)
        is_ent, purity = verify_entanglement(rho)
        # For I/4, reduced state is I/2 (purity 0.5).
        self.assertAlmostEqual(purity, 0.5)
        # Current logic (purity < 0.99) will flag this as entangled.
        # This documents the current heuristic limitation for mixed states.
        self.assertTrue(is_ent) 

    def test_verify_entanglement_subsystems(self):
        # GHZ state: (|000> + |111>)/sqrt(2)
        psi = (Statevector.from_label('000') + Statevector.from_label('111')) / np.sqrt(2)
        # Trace out qubit 1 (middle)
        is_ent, purity = verify_entanglement(psi, subsystem_to_trace=[1])
        self.assertTrue(is_ent)
        self.assertAlmostEqual(purity, 0.5)

    def test_is_entangled_convenience(self):
        psi = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
        self.assertTrue(is_entangled(psi))
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

    def test_helstrom_bound_custom_prior(self):
        # For orthogonal states, success should be 1.0 regardless of prior
        psi0 = Statevector.from_label('0')
        psi1 = Statevector.from_label('1')
        success, error = helstrom_bound(psi0, psi1, prior=0.8)
        self.assertAlmostEqual(success, 1.0)
        self.assertAlmostEqual(error, 0.0)

    def test_compute_concurrence(self):
        # Bell state: C=1
        phi_plus = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
        self.assertAlmostEqual(compute_concurrence(phi_plus), 1.0)
        self.assertAlmostEqual(compute_concurrence(Statevector.from_label('01')), 0.0)

        # Partially entangled state: cos(theta)|00> + sin(theta)|11>
        # C = |sin(2*theta)|
        theta = np.pi / 8
        psi = np.cos(theta) * Statevector.from_label('00') + np.sin(theta) * Statevector.from_label('11')
        self.assertAlmostEqual(compute_concurrence(psi), np.sin(2*theta))

    def test_concurrence_invalid_dim(self):
        with self.assertRaises(ValueError):
            compute_concurrence(Statevector.from_label('0'))

class TestEntanglementComparison(unittest.TestCase):
    """Reorganized tests from scripts/entanglement_comparison.py"""
    
    def setUp(self):
        # Case A: Standard Bell prep from |00>
        qc_z = QuantumCircuit(2)
        attach_bell_state_prep(qc_z, 0, 1)
        self.state_z = Statevector.from_label("00").evolve(qc_z)

        # Case B: Bell prep starting from |++> (then returning to |00>)
        qc_x = QuantumCircuit(2)
        qc_x.h([0, 1])
        qc_x.h([0, 1])
        attach_bell_state_prep(qc_x, 0, 1)
        self.state_x = Statevector.from_label("00").evolve(qc_x)

    def test_preparation_path_equivalence(self):
        # Both paths should produce the same state
        fid = compute_fidelity(self.state_z, self.state_x)
        td = compute_trace_distance(self.state_z, self.state_x)
        self.assertAlmostEqual(fid, 1.0)
        self.assertAlmostEqual(td, 0.0)

    def test_bell_state_properties(self):
        for state in [self.state_z, self.state_x]:
            self.assertAlmostEqual(state_purity(state), 1.0)
            self.assertTrue(is_entangled(state))
            self.assertAlmostEqual(compute_concurrence(state), 1.0)

if __name__ == "__main__":
    unittest.main()
