# algorithms/grover/logic.py
# This module assembles the high-level Grover iteration components.
# Inputs: n_qubits (int)
# Outputs: grover_diffuser (Gate)

from qiskit import QuantumCircuit
from factories.oracle_factory import get_phase_flip_oracle

def get_diffuser(n_qubits: int):
    """Constructs the Grover diffusion operator (H(2|0⟩⟨0|-I)H).

    This is the standard reflection-about-the-mean operator used in Grover's algorithm.
    """
    qc = QuantumCircuit(n_qubits, name="Diffuser")

    # 1. Enter Hadamard basis
    qc.h(range(n_qubits))

    # 2. Phase flip on |00...0> using the phase oracle
    zero_mark = '0' * n_qubits
    qc.append(get_phase_flip_oracle(n_qubits, zero_mark), range(n_qubits))

    # 3. Exit Hadamard basis
    qc.h(range(n_qubits))

    return qc.to_gate()

