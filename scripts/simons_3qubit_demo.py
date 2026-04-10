# /scripts/simons_3qubit_demo.py
"""
Demo script for 3-qubit Simon's Algorithm using the modular structure + custom visualization.
"""


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.simons.logic import simons_algorithm_3qubit
from factories import create_simon_oracle           
from utils.visualization import show_circuit, show_quantum_object
from qiskit_aer import Aer
from qiskit import transpile, QuantumCircuit
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt


def run_simon_demo(secret: str = "110", shots: int = 8192, save_plots: bool = True):
    """
    Runs and visualizes 3-qubit Simon's Algorithm.
    """
    print(f"=== 3-Qubit Simon's Algorithm ===\nSecret string s = {secret}\n")

    # 1. Generate the full circuit
    qc = simons_algorithm_3qubit(secret)

    # Create output directory
    if save_plots:
        os.makedirs("output/simons", exist_ok=True)
        circuit_path = f"output/simons/simon_circuit_s={secret}.png"

    print(f"Circuit depth: {qc.depth()}")
    print(f"Total qubits: {qc.num_qubits}\n")

    # Show full circuit
    show_circuit(qc, label=f"3-Qubit Simon's Algorithm (s = {secret})", 
                 save_path=circuit_path if save_plots else None)

    # Show oracle separately
    oracle_gate = create_simon_oracle(secret)
    oracle_circuit = oracle_gate.definition
    show_circuit(oracle_circuit, 
                 label=f"Simon Oracle for s = {secret}", 
                 save_path=f"output/simons/simon_oracle_s={secret}.png" if save_plots else None)

    # 3. Simulate
    backend = Aer.get_backend('qasm_simulator')
    tqc = transpile(qc, backend=backend)
    result = backend.run(tqc, shots=shots).result()
    counts = result.get_counts(qc)

    print("\n=== Measurement Results (Input Register) ===")
    for bitstring, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {bitstring}: {count:5d}  ({count/shots*100:5.1f}%)")

    # Histogram
    plt.figure(figsize=(10, 6))
    plt.bar(counts.keys(), counts.values())
    plt.title(f"Simon's Algorithm - Secret String s = {secret}")
    plt.xlabel("Measured bitstrings (input register)")
    plt.ylabel("Counts")
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)

    if save_plots:
        hist_path = f"output/simons/simon_histogram_s={secret}.png"
        plt.savefig(hist_path)
        print(f"\n[Visualized] Histogram saved to: {hist_path}")
    plt.show()

    # Theoretical valid y values
    print("\n=== Theoretical Expected Results ===")
    print("Valid y satisfy  y · s = 0  (mod 2)")
    s_int = int(secret, 2)
    for y in range(8):
        y_bin = f"{y:03b}"
        if bin(y & s_int).count('1') % 2 == 0:
            print(f"   {y_bin}")

    # Post-oracle state (optional)
    print("\n=== Post-Oracle State (text only) ===")
    qc_oracle = QuantumCircuit(6)
    qc_oracle.h(range(3))
    qc_oracle.append(create_simon_oracle(secret), range(6))
    state = Statevector.from_instruction(qc_oracle)
    show_quantum_object(state, label="State after Simon Oracle")


if __name__ == "__main__":
    run_simon_demo(secret="110")