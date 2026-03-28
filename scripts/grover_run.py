# scripts/grover_run.py
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit import QuantumCircuit
from factories import get_phase_flip_oracle
from algorithms.grover.logic import get_diffuser   
from analysis.simulation import run_simulation, report_results
from analysis.resources import get_resource_report, print_resource_table, estimate_physical_overhead

def run_grover_search(n_qubits, target_state):
    N = 2**n_qubits
    num_iterations = int(np.floor(np.pi/4 * np.sqrt(N)))
    
    print(f"--- Grover Search: |{target_state}> on {n_qubits} qubits ---")
    print(f"Optimal iterations: {num_iterations}\n")

    # 1. Initialize Circuit
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    
    # 2. Build Iterations
    oracle = get_phase_flip_oracle(n_qubits, target_state)
    diffuser = get_diffuser(n_qubits)

    for _ in range(num_iterations):
        qc.append(oracle, range(n_qubits))
        qc.append(diffuser, range(n_qubits))
    
    # --- RESOURCE ANALYSIS BLOCK ---
    # Analyze the circuit before adding measurements
    resources = get_resource_report(qc)
    resources["Label"] = f"Grover-{n_qubits}Q"
    
    print("### Logical Resource Estimates (Clifford+T)")
    print_resource_table([resources])
    
    # Physical Overhead Estimation
    physical_stats = estimate_physical_overhead(n_qubits)
    print("\n### Physical Overhead (Surface Code d=15)")
    for key, value in physical_stats.items():
        print(f"{key}: {value}")
    print("-" * 40 + "\n")
    # -------------------------------

    qc.measure_all()

    # 3. Execute and Report
    counts, probabilities = run_simulation(qc)
    report_results(counts, probabilities)
    
    most_probable = max(counts, key=counts.get)
    if most_probable == target_state:
         print(f"Success: |{most_probable}> matches target.")

if __name__ == "__main__":
    run_grover_search(n_qubits=3, target_state="101")