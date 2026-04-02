# analysis/simulation.py
# path_to_file: analysis/simulation.py
# This module provides execution and diagnostic reporting for quantum circuits.

from qiskit_aer import AerSimulator
from qiskit import transpile
import pandas as pd

def run_simulation(circuit, shots=1024):
    # Function Constraints: Executes circuit and returns counts/probabilities.
    # What it does: Transpiles custom gates and returns counts/probabilities.
    # Inputs: circuit (QuantumCircuit), shots (int)
    # Outputs: tuple (counts, probabilities)
    
    backend = AerSimulator()
    
    # CRITICAL: Transpile the circuit to decompose custom factory gates
    # into basis gates (H, CX, P, etc.) that the simulator understands.
    compiled_circuit = transpile(circuit, backend)
    
    job = backend.run(compiled_circuit, shots=shots)
    result = job.result()
    
    counts = result.get_counts()
    
    # Calculate probabilities based on actual total shots received
    total_shots = sum(counts.values())
    probabilities = {k: v / total_shots for k, v in counts.items()}
    
    return counts, probabilities

def report_results(counts, probabilities):
    # Function Constraints: Prints a structured DataFrame of simulation results.
    # Inputs: counts (dict), probabilities (dict)
    # Outputs: None (Prints to console)
    data = {
        "Outcome": list(counts.keys()),
        "Frequency": list(counts.values()),
        "Probability": [f"{p:.2%}" for p in probabilities.values()]
    }
    df = pd.DataFrame(data).sort_values(by="Outcome")
    
    print("\n--- Execution Report ---")
    print(df.to_string(index=False))
    print("------------------------\n")