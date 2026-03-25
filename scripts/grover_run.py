# scripts/grover_run.py
# Function Constraints: Assembles and runs the Grover iterations.
# This script uses the centralized factories hub for modular components.

import sys
import os
import numpy as np

# Append project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit import QuantumCircuit
from factories import get_phase_flip_oracle, get_diffuser
from analysis.simulation import run_simulation, report_results

def run_grover_search(n_qubits, target_state):
    # 1. Calculate Optimal Iterations: floor(pi/4 * sqrt(N))
    N = 2**n_qubits
    num_iterations = int(np.floor(np.pi/4 * np.sqrt(N)))
    
    print(f"--- Grover Search: |{target_state}> on {n_qubits} qubits ---")
    print(f"Optimal iterations: {num_iterations}")

    # 2. Initialize Circuit to Uniform Superposition
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    
    # 3. Retrieve Components from Factories
    oracle = get_phase_flip_oracle(n_qubits, target_state)
    diffuser = get_diffuser(n_qubits)

    # 4. Amplitude Amplification Loop
    # Each iteration rotates the state vector closer to the target state.
    for _ in range(num_iterations):
        qc.append(oracle, range(n_qubits))
        qc.append(diffuser, range(n_qubits))
    
    qc.measure_all()

    # 5. Execute and Report
    counts, probabilities = run_simulation(qc)
    report_results(counts, probabilities)
    
    # Verify the most probable outcome matches target
    # Note: Qiskit results are little-endian (right-to-left)
    most_probable = max(counts, key=counts.get)
    # If your target_state is '101' (q2q1q0), most_probable will be '101'
    if most_probable == target_state:
         print(f"Success: Most probable state |{most_probable}> matches target.")

if __name__ == "__main__":
    run_grover_search(n_qubits=3, target_state="101")