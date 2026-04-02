# scripts/entanglement_comparison.py
# This script compares Z-basis (|00>) vs X-basis (|++>) entanglement prep.

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from factories import X_BASIS, Z_BASIS, attach_bell_state_prep
from analysis.simulation import run_simulation, report_results
from qiskit import QuantumCircuit

def run_comparison():
    # Comparing how different input bases affect the final Bell state
    print("ANALYZING ENTANGLEMENT DYNAMICS\n" + "="*40)
    
    # Case A: Standard Z-basis |00> -> |Phi+>
    qc_z = QuantumCircuit(2)
    attach_bell_state_prep(qc_z, 0, 1)
    qc_z.measure_all()
    
    # Case B: X-basis |++> -> ?
    # (Applying H-CX to |++> actually results in a different state)
    qc_x = QuantumCircuit(2)
    qc_x.h([0, 1]) # Prepare |++>
    attach_bell_state_prep(qc_x, 0, 1)
    qc_x.measure_all()

    print("--- Case A: Z-basis Input (|00>) ---")
    counts_z, _ = run_simulation(qc_z)
    print(counts_z)

    print("\n--- Case B: X-basis Input (|++>) ---")
    counts_x, _ = run_simulation(qc_x)
    print(counts_x)

if __name__ == "__main__":
    run_comparison()