import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from factories.primitive_factory import attach_bell_state_prep
from analysis.fidelity import compute_fidelity
from analysis.entanglement import is_entangled, compute_concurrence

class TestEntanglementComparisonLogic(unittest.TestCase):
    def test_case_a_logic(self):
        """Verify Case A: Starting from Z-basis |00>"""
        qc = QuantumCircuit(2)
        attach_bell_state_prep(qc, 0, 1)
        
        # Ideal state vector from |00>
        state = Statevector.from_label("00").evolve(qc)
        
        # Expected Bell state: (|00> + |11>)/sqrt(2)
        expected = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
        
        self.assertAlmostEqual(compute_fidelity(state, expected), 1.0)
        self.assertTrue(is_entangled(state))
        self.assertAlmostEqual(compute_concurrence(state), 1.0)

    def test_case_b_logic(self):
        """Verify Case B: Starting from X-basis |++>"""
        qc = QuantumCircuit(2)
        qc.h([0, 1])                            # Prepare |++>
        
        qc.h([0, 1])                            # Return to |00>
        attach_bell_state_prep(qc, 0, 1)        # Then apply standard Bell prep
        
        state = Statevector.from_label("00").evolve(qc)
        expected = (Statevector.from_label('00') + Statevector.from_label('11')) / np.sqrt(2)
        
        self.assertAlmostEqual(compute_fidelity(state, expected), 1.0)
        self.assertTrue(is_entangled(state))
        self.assertAlmostEqual(compute_concurrence(state), 1.0)

    def test_comparison_fidelity(self):
        """Verify that both paths result in the same state"""
        # Path A
        qc_a = QuantumCircuit(2)
        attach_bell_state_prep(qc_a, 0, 1)
        state_a = Statevector.from_label("00").evolve(qc_a)

        # Path B
        qc_b = QuantumCircuit(2)
        qc_b.h([0, 1])
        qc_b.h([0, 1])
        attach_bell_state_prep(qc_b, 0, 1)
        state_b = Statevector.from_label("00").evolve(qc_b)

        fid = compute_fidelity(state_a, state_b)
        self.assertAlmostEqual(fid, 1.0)

if __name__ == "__main__":
    unittest.main()
