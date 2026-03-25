# analysis/kickback.py
# This module provides utilities to detect phase kickback by comparing 
# quantum states before and after oracle evolution.

import numpy as np
from qiskit.quantum_info import Statevector

def verify_kickback(pre_state: Statevector, post_state: Statevector):
    # Function Constraints: Compares two states to identify relative phase or bit flips.
    # What it does: Detects if a transformation occurred beyond a simple global phase.
    # Inputs: pre_state (Statevector), post_state (Statevector)
    # Outputs: kickback_detected (bool), global_phase (float)
    
    # 1. Check for physical equivalence (ignores global phase)
    is_equivalent = pre_state.equiv(post_state)
    kickback_detected = not is_equivalent
    
    # 2. Calculate Global Phase
    # We find the first index where the amplitude is non-zero to find the phase ratio
    pre_data = pre_state.data
    post_data = post_state.data
    
    # Find index of the largest magnitude element to ensure numerical stability
    idx = np.argmax(np.abs(pre_data))
    
    # Ratio: post = pre * e^(i*theta) -> e^(i*theta) = post/pre
    phase_factor = post_data[idx] / pre_data[idx]
    global_phase = np.angle(phase_factor)
    
    return kickback_detected, global_phase

def report_phase_diagnostics(kickback_detected: bool, global_phase: float):
    # Function Constraints: Provides a human-readable summary of the phase analysis.
    # Inputs: kickback_detected (bool), global_phase (float)
    
    phase_deg = np.degrees(global_phase)
    
    print("\n--- Phase Diagnostic Report ---")
    print(f"Kickback Detected: {kickback_detected}")
    print(f"Global Phase:      {global_phase:.4f} rad ({phase_deg:.1f}°)")
    
    if not kickback_detected and abs(global_phase) > 0.01:
        print("Status: System underwent a Global Phase shift (Physically Identical).")
    elif kickback_detected:
        print("Status: Relative Phase Kickback detected (Physically Changed).")
    print("-------------------------------\n")