# /scripts/bernstein_vazirani_demo.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

 
from algorithms.bernstein_vazirani.logic import (
    get_bernstein_vazirani_circuit,
    analyze_phase_kickback
)
from analysis.kickback import verify_kickback, report_phase_diagnostics
from utils.visualization import show_circuit

def run_bv_demo(secret: str = "101", shots: int = 2048):
    """Run the full Bernstein-Vazirani circuit and show results."""
    print(f"\n=== Bernstein-Vazirani Demo ===")
    print(f"Secret string s = '{secret}'   (n = {len(secret)} qubits)")
    print("-" * 60)

    # Build circuit
    qc = get_bernstein_vazirani_circuit(secret)
    show_circuit(qc, label=f"Bernstein-Vazirani Circuit (secret = {secret})")
    
    # Run on simulator
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)
    
    # Get the most probable outcome
    measured = max(counts, key=counts.get)
    success = measured == secret
    
    print(f"Measured result:      {measured}")
    print(f"Expected secret:      {secret}")
    print(f"Success:              {success}")
    print(f"Total shots:          {shots}")
    print(f"Counts (top):         {dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:6])}")
    
    if success:
        print("✓ Secret recovered perfectly with a single query!")
    else:
        print("✗ Failed — this should not happen with enough shots.")
    
    return qc, counts





def main():
    """Run demonstrations for several secret strings."""
    print("Bernstein-Vazirani Algorithm - Demo Script")
    print("=" * 70)
    
    test_secrets = ["101", "1101", "0110", "111", "10101"]
    
    for secret in test_secrets:
        run_bv_demo(secret)
        analyze_phase_kickback(secret)
        print("\n" + "=" * 70)
    
    
    print("Key takeaway: Bernstein-Vazirani recovers the hidden n-bit string")
    print("              using only ONE query to the oracle.")


if __name__ == "__main__":
    main()