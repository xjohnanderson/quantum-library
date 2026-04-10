# analysis/measurement.py
# Script: Utilities for simulating and verifying state collapse after measurement.

def simulate_measurement(state, qubits):
    # Function Constraints: Measures specific qubits and returns result + collapsed state.
    # Inputs: state (Statevector), qubits (list of int)
    # Outputs: result (str), collapsed_state (Statevector)
    result, collapsed_state = state.measure(qubits)
    return result, collapsed_state