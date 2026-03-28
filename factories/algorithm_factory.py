# factories/algorithm_factory.py
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

"""Fourier Transform"""
def get_iqft_circuit(n_qubits: int, do_swaps: bool = True) -> QuantumCircuit:
    # Returns the Inverse Quantum Fourier Transform (IQFT) circuit.

    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1.")

    iqft = QFT(
        num_qubits=n_qubits,
        approximation_degree=0,
        do_swaps=do_swaps,
        inverse=True,
        name="IQFT"
    )
    # Return as circuit (most convenient for appending)
    return iqft


def get_qft_circuit(n_qubits: int, do_swaps: bool = True) -> QuantumCircuit:
    # Returns the (forward) Quantum Fourier Transform circuit
    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1.")

    qft = QFT(
        num_qubits=n_qubits,
        approximation_degree=0,
        do_swaps=do_swaps,
        inverse=False,
        name="QFT"
    )
    return qft
"""End Fourier Transform"""


