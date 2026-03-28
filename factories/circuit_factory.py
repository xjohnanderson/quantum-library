# factories/circuit_factory.py
# Reusable circuit components, gates, oracles, and circuit templates.

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import ZGate, QFT, PauliEvolutionGate
from qiskit.quantum_info import Operator, SparsePauliOp
from utils.math_ops import get_mod_inv
import numpy as np









"""Custom Gates"""
def get_rfa_gate():
    # Function Constraints: Defines a Reversible Full Adder (RFA).
    # Inputs: None
    # Outputs: rfa_gate (Gate)
    
    qa = QuantumRegister(1, 'A')
    qb = QuantumRegister(1, 'B')
    qcin = QuantumRegister(1, 'Cin')
    qs = QuantumRegister(1, 'S')
    qcout = QuantumRegister(1, 'Cout')
    
    qc = QuantumCircuit(qa, qb, qcin, qs, qcout, name='RFA')
    
    # Logic: S = A ^ B ^ Cin | Cout = (A & B) | (Cin & (A ^ B))
    qc.cx(0, 3)     # A to Sum
    qc.cx(1, 3)     # B to Sum
    qc.ccx(0, 1, 4) # A & B to Cout
    qc.ccx(2, 3, 4) # Cin & Sum_intermediate to Cout
    qc.cx(2, 3)     # Final Sum
    
    return qc.to_gate(label='RFA')


def get_modular_multiplier_gate(a, N):
    # Function Constraints: Implements the unitary permutation |x> -> |a*x mod N>.
    n_bits = int(np.ceil(np.log2(N)))
    U = np.zeros((2**n_bits, 2**n_bits))
    
    for x in range(2**n_bits):
        if x < N:
            U[(a * x) % N, x] = 1
        else:
            U[x, x] = 1 
            
    return Operator(U)
"""End Custom Gates"""


""" State Prep """
def get_x_basis_prep_circuit(state_symbols):
    # Function Constraints: Returns a circuit to prepare a multi-qubit X-basis state.
    # Inputs: state_symbols (str e.g., "+-")
    # Outputs: QuantumCircuit
    n = len(state_symbols)
    qc = QuantumCircuit(n, name=f"Prep_{state_symbols}")
    
    for i, symbol in enumerate(reversed(state_symbols)):
        if symbol == '-':
            qc.x(i)
        qc.h(i)
    return qc
""" End State Prep """


"""Operator Utilities """
def get_composite_operator(labels: list):
    # Create multi-qubit Operator from list of single-qubit labels.
    op = Operator.from_label(labels[0])
    for label in labels[1:]:
        op = op.tensor(Operator.from_label(label))
    return op

def get_evolution_circuit() -> QuantumCircuit:
    # Example custom single-qubit evolution: H-T-H-S-Y
    qc = QuantumCircuit(1, name="CustomEvolution")
    qc.h(0)
    qc.t(0)
    qc.h(0)
    qc.s(0)
    qc.y(0)
    return qc

def get_circuit_operator(circuit: QuantumCircuit):
    # Convert any circuit to its unitary Operator
    return Operator.from_circuit(circuit)
"""End Operator Utilities"""



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


""" Optimization Hamiltonian """
def get_pauli_op(n_qubits: int, linear: dict, quadratic: dict) -> SparsePauliOp:
    # Function Constraints: Maps QUBO coefficients to a SparsePauliOp.
    # Inputs: n_qubits (int), linear (dict {index: weight}), quadratic (dict {(i, j): weight})
    pauli_list = []
    
    for i, w in linear.items():
        # Map x_i -> 0.5 * (I - Z_i)
        op_str = ["I"] * n_qubits
        op_str[i] = "Z"
        pauli_list.append(("".join(reversed(op_str)), -0.5 * w))
        
    for (i, j), w in quadratic.items():
        # Map x_i*x_j -> 0.25 * (I - Z_i - Z_j + Z_i*Z_j)
        # Note: Usually simplified to Z_i*Z_j interactions for Ising
        op_str = ["I"] * n_qubits
        op_str[i] = "Z"
        op_str[j] = "Z"
        pauli_list.append(("".join(reversed(op_str)), 0.25 * w))
        
    return SparsePauliOp.from_list(pauli_list)

def get_hamiltonian_evolution_gate(pauli_op: SparsePauliOp, time: float) -> PauliEvolutionGate:
    # Function Constraints: Converts a Hamiltonian into a unitary evolution gate e^-iHt.
    return PauliEvolutionGate(pauli_op, time=time)
"""End Optimization Hamiltonian"""