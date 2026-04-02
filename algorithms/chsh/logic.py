# algorithms/chsh/logic.py
# This script implements the Quantum Strategy for the CHSH game.

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from factories.primitive_factory import attach_bell_state_prep


def quantum_strategy(x: int, y: int):
    # Function Constraints: Executes a single-shot simulation for the CHSH game.
    # Outputs: tuple (a, b) as strings
    sim = AerSimulator()
    job = sim.run(get_chsh_circuit(x, y), shots=1, memory=True)
    result = job.result().get_memory()[0] # 'ba'
    return result[1], result[0]



"""CHSH Game"""
def get_chsh_circuit(x: int, y: int) -> QuantumCircuit:
    # Constructs a 2-qubit CHSH circuit for measurement settings (x, y)

    if x not in (0, 1) or y not in (0, 1):
        raise ValueError("x and y must be 0 or 1.")
    
    qc = QuantumCircuit(2, 2, name=f"CHSH_x{x}_y{y}")
    
    # 1. Prepare Shared Entanglement (Phi+)
    attach_bell_state_prep(qc, 0, 1)
    qc.barrier()
    
    # 2. Alice's Basis Rotation (x=0: Z-basis, x=1: X-basis)
    if x == 1:
        qc.ry(-np.pi / 2, 0)
        
    # 3. Bob's Basis Rotation (y=0: W1, y=1: W2)
    # Angles are pi/8 and -pi/8 relative to Alice's bases.
    theta_b = -np.pi / 4 if y == 0 else np.pi / 4
    qc.ry(theta_b, 1)
        
    qc.measure([0, 1], [0, 1])
    return qc
"""End CHSH Game"""