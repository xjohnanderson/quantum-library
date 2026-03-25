# scripts/shor_factor_demo.py 
# Demo: Factoring 15 using modular components.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 

import numpy as np
from math import gcd
from qiskit_aer import Aer, AerSimulator
from qiskit import transpile
from algorithms.shors.logic import create_shor_circuit
from factories.circuit_factory import get_modular_multiplier_gate
from utils.math_ops import get_period_from_phase

def run_shor_factorization(N, a):
    # Function Constraints: Orchestrates the quantum and classical steps of factorization.
    # Inputs: N (int), a (int)
    # Outputs: None (Prints results)
    
    print(f"--- Factoring N = {N} using base a = {a} ---")
    
    # 1. Parameter Setup
    n_count = 8  # Number of counting qubits for phase precision
    n_target = int(np.ceil(np.log2(N)))
    
    # 2. Prepare the Modular Exponentiation Gate
    # Logic: Construct a controlled modular multiplication gate U: |x> -> |a*x mod N>
    U = get_modular_multiplier_gate(a, N)
    modular_exp_gate = U.to_instruction().control(1)
    
    # 3. Build the Circuit via algorithms/shors/logic.py
    # We pass the gate for a single U application. 
    # Note: For a true period finder, one usually passes a power-of-two sequence.
    # Here we demonstrate the modular structure.
    qc = create_shor_circuit(n_count, n_target, modular_exp_gate)
    
    # 4. Simulation
   # Initialize the modern simulator
    simulator = AerSimulator()

    # CRITICAL: Transpile the circuit to decompose 'c-unitary' into basis gates
    # This maps the high-level logic to instructions the C++ backend understands.
    t_qc = transpile(qc, simulator)

    # Run the transpiled circuit with memory enabled for the readout
    job = simulator.run(t_qc, shots=1, memory=True)
    result = job.result()
    
    # Access the raw bitstring from memory
    readout = result.get_memory()[0]
    measured_int = int(readout, 2)
    
    print(f"Quantum Measurement: {readout} (Decimal: {measured_int})")
    
    # 5. Classical Post-Processing via utils/math_ops.py
    r = get_period_from_phase(measured_int, n_count, N)
    print(f"Candidate Period r: {r}")
    
    # 6. Factor Verification
    if r % 2 == 0:
        x = pow(a, r//2, N)
        if (x + 1) % N != 0:
            factor1 = gcd(x - 1, N)
            factor2 = gcd(x + 1, N)
            print(f"Success! Factors found: {factor1} and {factor2}")
        else:
            print("Failure: r found but (a^{r/2} + 1) is a multiple of N.")
    else:
        print("Failure: Measured period r is odd.")

if __name__ == "__main__":
    # Standard test case: 15 = 3 * 5, using a=7
    run_shor_factorization(15, 7)