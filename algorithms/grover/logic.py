# algorithms/grover/logic.py
# This module assembles the high-level Grover iteration components.
# Inputs: n_qubits (int)
# Outputs: grover_diffuser (Gate)

from qiskit import QuantumCircuit
from factories.oracle_factory import get_phase_flip_oracle

def create_grover_diffuser(n_qubits):
    # Function Constraints: Constructs the Grover diffusion operator H(2|0><0|-I)H.
    # What it does: Uses a phase oracle targeting |0...0> wrapped in Hadamards.
    # Inputs: n_qubits (int)
    # Outputs: diffuser_gate (Gate)
    
    qc = QuantumCircuit(n_qubits, name="GroverDiffuser")
    
    # 1. Transform to Hadamard basis
    qc.h(range(n_qubits))
    
    # 2. Apply the phase flip oracle targeting the |0...0> state
    # This effectively implements the (2|0><0| - I) logic
    zero_target = '0' * n_qubits
    diffuser_core = get_phase_flip_oracle(n_qubits, zero_target)
    qc.append(diffuser_core, range(n_qubits))
    
    # 3. Transform back from Hadamard basis
    qc.h(range(n_qubits))
    
    # Return as a gate for modular assembly in larger Grover circuits
    return qc.to_gate()