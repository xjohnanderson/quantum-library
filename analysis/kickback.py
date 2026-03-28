# analysis/kickback.py

import numpy as np
from qiskit.quantum_info import Statevector, state_fidelity

def verify_kickback(pre_state: Statevector, post_state: Statevector):
    """
    Determines if a relative phase (kickback) occurred by checking 
    if states are physically distinguishable beyond a global phase.
    """
    # Fidelity is 1.0 if states are identical up to a global phase
    fidelity = state_fidelity(pre_state, post_state)
    is_equivalent = np.isclose(fidelity, 1.0)
    kickback_detected = not is_equivalent
    
    # Calculate global phase: <pre|post> = e^(i*theta)
    # Using the inner product is more stable than picking one index
    inner_product = np.vdot(pre_state.data, post_state.data)
    global_phase = np.angle(inner_product)
    
    return kickback_detected, global_phase

def report_phase_diagnostics(kickback_detected: bool, global_phase: float):
    phase_deg = np.degrees(global_phase)
    
    print("\n--- Phase Diagnostic Report ---")
    print(f"Kickback Detected: {kickback_detected}")
    print(f"Phase Shift:       {global_phase:.4f} rad ({phase_deg:.1f}°)")
    
    status = ("Relative Phase Kickback (Information encoded)" if kickback_detected 
              else "Global Phase Shift (No information encoded)")
    print(f"Status: {status}")
    print("-------------------------------\n")