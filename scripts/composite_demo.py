# scripts/composite_demo.py
# Demo: Exploring multi-qubit systems, tensor products, and measurement collapse.
# This script integrates the IBM Composite Systems logic into the modular library.

import sys
import os
from qiskit.quantum_info import Statevector, Operator
from qiskit.circuit.library import CXGate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from factories import Z_BASIS, get_w_state, get_composite_operator
from utils.visualization import show_state, show_operator
from analysis.measurement import simulate_measurement

def run_composite_demonstration():
    # 1. State Composition (Tensor Products)
    # Using Z_BASIS logic: |0> tensor |1> = |01>
    # Note: Qiskit uses little-endian ordering (q1 ⊗ q0)
    zero = Statevector.from_label('0')
    one = Statevector.from_label('1')
    
    psi = zero.tensor(one) 
    show_state(psi, "Composite State |0> ⊗ |1>")

    # 2. Operator Composition
    # Creating H ⊗ I ⊗ X using the composite factory
    # This results in an 8x8 matrix representing the 3-qubit transformation.
    tri_op = get_composite_operator(['H', 'I', 'X'])
    show_operator(tri_op, "Composite Operator H ⊗ I ⊗ X")

    # 3. Evolution of Composite Systems (Entanglement)
    # Prepare |+> ⊗ |0>
    plus = Statevector.from_label('+')
    initial_bipartite = plus.tensor(zero)
    
    # FIX: Correctly instantiate the CX (CNOT) Operator
    cx_op = Operator(CXGate()) 
    
    entangled_state = initial_bipartite.evolve(cx_op)
    show_state(entangled_state, "Entangled State (Bell State via CX)")

    # 4. Measurement and State Collapse (W-State)
    # The W-state: (|001> + |010> + |100>) / sqrt(3)
    w_state = get_w_state()
    show_state(w_state, "Initial 3-Qubit W-State")

    # Partial Measurement on qubit 0
    # This demonstrates the 'Measurement Collapse' phenomenon.
    res, collapsed_state = simulate_measurement(w_state, [0])
    print(f"\n[Measurement Result on Qubit 0]: {res}")
    show_state(collapsed_state, "State After Partial Measurement [0]")

if __name__ == "__main__":
    run_composite_demonstration()