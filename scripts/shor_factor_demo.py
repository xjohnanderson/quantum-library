# scripts/shor_factor_demo.py
import sys
import os
import numpy as np
from math import gcd
from qiskit_aer import AerSimulator
from qiskit import transpile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.shors.logic import create_shor_circuit
from utils.math_ops import get_period_from_phase
from utils.visualization import show_circuit

def run_shor_factorization(N: int, a: int):
    print(f"=== Shor’s Algorithm (Matrix Version) ===")
    print(f"Factoring N = {N} using base a = {a}\n")
    
    if gcd(a, N) != 1:
        print("❌ ERROR: a and N are not coprime — choose different a.")
        return

    n_count = 8
    qc = create_shor_circuit(n_count, a, N)

    show_circuit(qc, label=f"Shor Circuit (Matrix) - N={N}, a={a}")

    simulator = AerSimulator()
    t_qc = transpile(qc, simulator, optimization_level=2)

    result = simulator.run(t_qc, shots=1024).result()
    counts = result.get_counts()

    measured = max(counts, key=counts.get)
    measured_int = int(measured, 2)
    print(f"Most frequent measurement: {measured} (decimal: {measured_int})")
    print(f"Counts: {counts[measured]} / 1024")

    r = get_period_from_phase(measured_int, n_count, N, a)
    print(f"Estimated period r = {r}")

    if r > 0 and r % 2 == 0:
        x = pow(a, r // 2, N)
        if x != N - 1:
            factor1 = gcd(x - 1, N)
            factor2 = gcd(x + 1, N)
            if 1 < factor1 < N and 1 < factor2 < N:
                print(f"✅ SUCCESS! Factors: {factor1} and {factor2}")
            else:
                print("Period found but factors trivial — retry with more shots.")
        else:
            print("Failure: (a^{r/2} + 1) ≡ 0 mod N")
    else:
        print("Odd period or invalid r — typical in Shor. Retry with different a or more shots.")


if __name__ == "__main__":
    run_shor_factorization(15, 7)   # Classic demo
    # run_shor_factorization(21, 5)   # Try larger N