# analysis/entanglement.py
# This module provides utilities for verifying quantum correlations and state purity.

from qiskit.quantum_info import Statevector, partial_trace

def verify_entanglement(state: Statevector):
    # Function Constraints: Checks if a bipartite state is entangled via purity of the reduced density matrix.
    # Inputs: state (Statevector)
    # Outputs: is_entangled (bool), purity (float)
    
    # Trace out the second qubit to inspect the local state of the first
    rho = partial_trace(state, [1]) 
    purity = rho.purity()
    
    # Logic: A pure global state is entangled if its local subsystems are mixed.
    # Purity = 1.0 (Separable/Pure), Purity < 1.0 (Entangled/Mixed)
    is_entangled = purity < 0.999  # Using a small epsilon for float precision
    return is_entangled, purity