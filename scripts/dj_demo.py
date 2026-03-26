# scripts/dj_demo.py
# Demo of Deutsch-Jozsa algorithm for n=3 qubits.

from factories.circuit_factory import get_deutsch_jozsa_circuit
from analysis.dj_verification import verify_dj_result
from utils.visualization import show_quantum_object
from qiskit import execute, Aer

def run_demo():
    n = 3
    cases = ['constant_0', 'balanced']
    simulator = Aer.get_backend('qasm_simulator')
    
    for case in cases:
        print(f"\n{'='*20}\nDEMO: {case.upper()} CASE\n{'='*20}")
        
        # 1. Get Circuit
        qc = get_deutsch_jozsa_circuit(n, case)
        
        # 2. Visualize Circuit (ASCII/LaTeX)
        show_quantum_object(qc, label=f"Circuit for {case}")
        
        # 3. Execute
        job = execute(qc, simulator, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        # 4. Verify and Output
        analysis = verify_dj_result(counts, n)
        
        print(f"Detected Function Type: {analysis['classification']}")
        print(f"Probability of |000>: {analysis['prob_all_zeros']}")
        print(f"Measurement Counts: {analysis['raw_counts']}")

if __name__ == "__main__":
    run_demo()