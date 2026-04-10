# scripts/fidelity_trace_distance_demo.py

import sys
import os

 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix

 
from factories.basis_factory import get_2qubit_z_basis, get_bell_basis
from factories.primitive_factory import attach_bell_state_prep
from analysis.fidelity import (
    compute_fidelity,
    compute_trace_distance,
    is_pure_state,
    create_mixed_state,
)


def main() -> None:
    print("Trace Distance & Fidelity Demo (Pure + Mixed States)\n")

    # Pure states  
    z_basis = get_2qubit_z_basis()          # dict: {'00': |00⟩, '01': |01⟩, ...}
    bell_states = get_bell_basis()          # dict: {'phi+': |Φ⁺⟩, ...}

    psi00 = z_basis['00']
    psi11 = z_basis['11']
    phi_plus = bell_states['phi+']          # standard Bell |Φ⁺⟩ = (|00⟩ + |11⟩)/√2

    print("Pure states created via factories:")
    print(f"  • |00⟩ purity = {is_pure_state(psi00)}")
    print(f"  • |Φ⁺⟩ purity = {is_pure_state(phi_plus)}\n")

    # Same state
    fid_same = compute_fidelity(psi00, psi00)
    td_same = compute_trace_distance(psi00, psi00)
    print(f"Fidelity(|00⟩, |00⟩)  = {fid_same:.6f}  (ideal = 1)")
    print(f"TraceDist(|00⟩, |00⟩) = {td_same:.6f}  (ideal = 0)\n")

    # Orthogonal pure states
    fid_orth = compute_fidelity(psi00, psi11)
    td_orth = compute_trace_distance(psi00, psi11)
    print(f"Fidelity(|00⟩, |11⟩)  = {fid_orth:.6f}  (ideal = 0)")
    print(f"TraceDist(|00⟩, |11⟩) = {td_orth:.6f}  (ideal = 1)\n")

    # Different pure states (1-qubit example)
    zero_1q = Statevector.from_label('0')
    plus_1q = Statevector.from_label('+')
    fid_zx = compute_fidelity(zero_1q, plus_1q)
    td_zx = compute_trace_distance(zero_1q, plus_1q)
    print(f"Fidelity(|0⟩, |+⟩)     = {fid_zx:.6f}")
    print(f"TraceDist(|0⟩, |+⟩)    = {td_zx:.6f}\n")

    bell_circ = QuantumCircuit(2)
    attach_bell_state_prep(bell_circ, 0, 1)     
    bell_sv = Statevector.from_label("00").evolve(bell_circ)

    fid_bell_00 = compute_fidelity(psi00, bell_sv)
    td_bell_00 = compute_trace_distance(psi00, bell_sv)
    print(f"Fidelity(|00⟩, |Φ⁺⟩)   = {fid_bell_00:.6f}")
    print(f"TraceDist(|00⟩, |Φ⁺⟩)  = {td_bell_00:.6f}\n")

    # Mixed states  
    # Classical mixture: 50% |00⟩ + 50% |11⟩
    mixed_00_11 = create_mixed_state([psi00, psi11], [0.5, 0.5])

    print("Mixed state (0.5|00⟩ + 0.5|11⟩):")
    print(f"  • Purity = {mixed_00_11.purity():.6f}  (mixed < 1)")
    print(f"  • Is pure? {is_pure_state(mixed_00_11)}\n")

    fid_mixed_pure = compute_fidelity(mixed_00_11, psi00)
    td_mixed_pure = compute_trace_distance(mixed_00_11, psi00)
    print(f"Fidelity(mixed, |00⟩)     = {fid_mixed_pure:.6f}")
    print(f"TraceDist(mixed, |00⟩)    = {td_mixed_pure:.6f}\n")

    # Another mixed state for comparison (e.g. depolarized Bell)
    depolarized_bell = 0.9 * DensityMatrix(phi_plus) + 0.1 * DensityMatrix.from_label("00")
    fid_dep_bell = compute_fidelity(depolarized_bell, phi_plus)
    td_dep_bell = compute_trace_distance(depolarized_bell, phi_plus)
    print("Depolarized Bell (|Φ⁺⟩ with 10% noise):")
    print(f"  • Fidelity with ideal |Φ⁺⟩ = {fid_dep_bell:.6f}")
    print(f"  • Trace distance             = {td_dep_bell:.6f}\n")

    try:
        from analysis.entanglement import state_purity  
        print(f"Cross-check purity via entanglement.py: {state_purity(mixed_00_11):.6f}")
    except ImportError:
        print("   (skipped: state_purity not found in analysis/entanglement.py)")

 

if __name__ == "__main__":
    main()