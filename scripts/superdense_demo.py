# scripts/superdense_demo.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.superdense.logic import get_superdense_circuit
from analysis.simulation import run_simulation, report_results

def run_demo():
    # Alice wants to send '10' (c=1, d=0)
    c, d = "1", "0"
    print(f"--- Superdense Coding Demo ---")
    print(f"Goal: Send bits c={c}, d={d} using one qubit via an entangled pair.")
    
    # 1. Build Circuit
    qc = get_superdense_circuit(c, d)
    
    # 2. Simulate
    counts, probabilities = run_simulation(qc)
    
    # 3. Report
    report_results(counts, probabilities)
    
    # 4. Verification Logic (Qiskit is little-endian: bitstring is 'dc')
    received = list(counts.keys())[0] 
    if received == d + c:
        print(f"[VERDICT] Success: Bob decoded '{received}' correctly.")

if __name__ == "__main__":
    run_demo()