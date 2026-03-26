# scripts/dj_demo.py
# Demo of Deutsch-Jozsa algorithm for n=3 qubits.
# Inputs: n (int). Outputs: Execution counts and verification.

import sys
import os
from qiskit import transpile
from qiskit_aer import AerSimulator

# Ensure the root is in the python path for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from factories.circuit_factory import get_deutsch_jozsa_circuit
from analysis.dj_verification import verify_dj_result
from utils.visualization import show_quantum_object

def run_demo():
    n = 3
    cases = ['constant_0', 'balanced']
    
    # Qiskit 1.x: Use AerSimulator directly
    simulator = AerSimulator()
    
    for case in cases:
        print(f"\n{'='*20}\nDEMO: {case.upper()} CASE\n{'='*20}")
        
        # 1. Get Circuit from your factory
        qc = get_deutsch_jozsa_circuit(n, case)
        
        # 2. Visualize Circuit (ASCII/LaTeX) via your utils
        show_quantum_object(qc, label=f"Circuit for {case}")
        
        # 3. Execute: Transpile first, then run
        # This is the modern replacement for the 'execute' wrapper
        compiled_circuit = transpile(qc, simulator)
        job = simulator.run(compiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        # 4. Verify and Output via your analysis module
        analysis = verify_dj_result(counts, n)
        
        print(f"Detected Function Type: {analysis['classification']}")
        print(f"Probability of |000>: {analysis.get('prob_all_zeros', 'N/A')}")
        print(f"Measurement Counts: {analysis['raw_counts']}")

if __name__ == "__main__":
    run_demo()