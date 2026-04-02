# analysis/fidelity.py
# Script: Tools for State Tomography and Fidelity Analysis.

import numpy as np
from qiskit.quantum_info import state_fidelity, DensityMatrix

def check_transfer_integrity(target_rho, bob_rho):
    # Function Constraints: Compares density matrices and calculates fidelity.
    # Inputs: target_rho (DensityMatrix), bob_rho (DensityMatrix)
    # Outputs: float (0.0 to 1.0)
    
    fid = state_fidelity(target_rho, bob_rho)
    is_match = np.allclose(target_rho.data, bob_rho.data, atol=1e-8)
    
    return fid, is_match