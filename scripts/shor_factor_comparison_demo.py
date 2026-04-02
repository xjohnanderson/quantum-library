# scripts/shor_factor_comparison_demo.py
import sys
import os
import numpy as np
from math import gcd
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit import transpile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports from the split factories + analysis + visualization
from algorithms.shors.logic import create_shor_circuit, create_shor_circuit_adder
from analysis.resources import get_resource_report, print_resource_table, estimate_physical_overhead
from utils.visualization import show_circuit
from utils.math_ops import get_period_from_phase


def run_comparison_demo(N: int = 15, a: int = 7):
    print(f"=== SHOR FACTORIZATION COMPARISON DEMO ===")
    print(f"N = {N} | a = {a}\n")

    if gcd(a, N) != 1:
        print("❌ a and N are not coprime.")
        return

    n_count = 8
    reports = []

    # 1. MATRIX VERSION (recommended — compact & fast)
    print("→ Running MATRIX version (compact)...")
    qc_matrix = create_shor_circuit(n_count, a, N)
    show_circuit(qc_matrix, label=f"Shor Circuit (Matrix) - N={N}, a={a}")

    resource_matrix = get_resource_report(qc_matrix)
    resource_matrix["Label"] = "Matrix Version"
    reports.append(resource_matrix)

    # 2. ADDER VERSION (scalable but wide)
    print("\n→ Running ADDER version  ...")
    qc_adder_full = create_shor_circuit_adder(n_count, a, N)
    show_circuit(qc_adder_full, label=f"Shor Circuit (Adder) - N={N}, a={a}")

    resource_adder = get_resource_report(qc_adder_full)
    resource_adder["Label"] = "Adder Version"
    reports.append(resource_adder)

    # Resource comparison table
    print("\n=== RESOURCE COMPARISON (Clifford+T basis) ===")
    print_resource_table(reports)

    # Physical overhead estimate
    print("\n=== PHYSICAL OVERHEAD ESTIMATE (Surface Code) ===")
    for r in reports:
        overhead = estimate_physical_overhead(r["Logical Qubits"])
        print(f"{r['Label']}: {overhead['Total Physical Qubits']} physical qubits "
              f"(d={overhead['Code Distance (d)']})")

    # Quick simulation of the recommended (matrix) version
    print("\n=== QUICK SIMULATION (Matrix version only) ===")
    simulator = AerSimulator()
    t_qc = transpile(qc_matrix, simulator, optimization_level=2)
    result = simulator.run(t_qc, shots=1024).result()
    counts = result.get_counts()

    measured = max(counts, key=counts.get)
    measured_int = int(measured, 2)
    r = get_period_from_phase(measured_int, n_count, N, a)
    print(f"Most frequent measurement: {measured} (decimal: {measured_int})")
    print(f"Estimated period r = {r}")

    if r > 0 and r % 2 == 0:
        x = pow(a, r // 2, N)
        f1 = gcd(x - 1, N)
        f2 = gcd(x + 1, N)
        if 1 < f1 < N and 1 < f2 < N:
            print(f"✅ SUCCESS! Factors: {f1} × {f2}")
        else:
            print("Trivial factors — try different a.")
    else:
        print("Odd period — typical in Shor.")


if __name__ == "__main__":
    # run_comparison_demo(N=15, a=7)
    run_comparison_demo(N=21, a=5)   # try larger N