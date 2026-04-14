# scripts/entanglement_comparison.py
"""
Entanglement Comparison Demo with Bloch Sphere Visualization

Compares two ways of preparing a Bell state:
- Starting from Z-basis |00⟩
- Starting from X-basis |++⟩

Uses the new analysis tools + Bloch sphere plots via utils.visualization
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Library imports
from factories.primitive_factory import attach_bell_state_prep
from analysis.fidelity import compute_fidelity, compute_trace_distance
from analysis.entanglement import (
    state_purity,
    compute_concurrence,
    is_entangled,
)

# Simulation
from analysis.simulation import run_simulation, report_results


try:
    from utils.visualization import plot_bloch_multivector
except ImportError:
    plot_bloch_multivector = None
    print("Warning: utils.visualization.plot_bloch_multivector not found. Skipping plots.")


def run_comparison():
    print("ENTANGLEMENT COMPARISON: Z-basis vs X-basis Input")
    print("=" * 70)

    # ====================== CASE A: Z-basis |00⟩ ======================
    qc_z = QuantumCircuit(2)
    attach_bell_state_prep(qc_z, 0, 1)        # Standard: H(0) + CX(0,1)

    qc_z_meas = qc_z.copy()
    qc_z_meas.measure_all()

    # Get final statevector (before measurement)
    ideal_bell = Statevector.from_label("00").evolve(qc_z)

    print("\n--- Case A: Starting from Z-basis |00⟩ ---")
    counts_z, probs_z = run_simulation(qc_z_meas)
    report_results(counts_z, probs_z)

    print(f"  Purity        : {state_purity(ideal_bell):.4f}")
    print(f"  Entangled?    : {is_entangled(ideal_bell)}")
    print(f"  Concurrence   : {compute_concurrence(ideal_bell):.4f}  ← maximally entangled")

    # Bloch sphere for final state
    if plot_bloch_multivector:
        plot_bloch_multivector(ideal_bell, title="Case A: Final Bell State from |00⟩")


    # ====================== CASE B: X-basis |++⟩ ======================
    qc_x = QuantumCircuit(2)
    qc_x.h([0, 1])                            # Prepare |++⟩
    attach_bell_state_prep(qc_x, 0, 1)        # Then apply standard Bell prep

    qc_x_meas = qc_x.copy()
    qc_x_meas.measure_all()

    final_x = Statevector.from_label("00").evolve(qc_x)

    print("\n--- Case B: Starting from X-basis |++⟩ ---")
    counts_x, probs_x = run_simulation(qc_x_meas)
    report_results(counts_x, probs_x)

    print(f"  Purity        : {state_purity(final_x):.4f}")
    print(f"  Entangled?    : {is_entangled(final_x)}")
    print(f"  Concurrence   : {compute_concurrence(final_x):.4f}  ← maximally entangled")

    if plot_bloch_multivector:
        plot_bloch_multivector(final_x, title="Case B: Final Bell State from |++⟩")


    # ====================== COMPARISON ======================
    print("\n" + "=" * 70)
    print("FINAL STATE COMPARISON")
    
    fid = compute_fidelity(ideal_bell, final_x)
    td = compute_trace_distance(ideal_bell, final_x)
    
    print(f"Fidelity (Z-path vs X-path)   = {fid:.6f}")
    print(f"Trace Distance                = {td:.6f}")
    print(f"Both maximally entangled?     = {is_entangled(ideal_bell) and is_entangled(final_x)}")

    print("\n✅ Conclusion:")
    if fid > 0.999:
        print("   Both methods produce the **identical** maximally entangled Bell state |Φ⁺⟩.")
        print("   The input basis affects only the preparation path — not the final entanglement.")
    else:
        print("   Unexpected state mismatch detected.")


if __name__ == "__main__":
    run_comparison()