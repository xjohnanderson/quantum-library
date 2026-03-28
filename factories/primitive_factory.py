# factories/primitive_factory.py

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator
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


"""Bell Protocol Helpers """
def attach_bell_state_prep(qc: QuantumCircuit, q0: int, q1: int) -> QuantumCircuit:
    # Appends H and CX to create a Phi+ |Φ+⟩ Bell state.
    qc.h(q0)
    qc.cx(q0, q1)
    return qc

def attach_bell_measurement(qc: QuantumCircuit, q_control: int, q_target: int) -> QuantumCircuit:
    # Appends CX + H for Bell-basis measurement
    qc.cx(q_control, q_target)
    qc.h(q_control)
    return qc
"""End Bell Protocol Helpers """

""" State Prep """
def get_x_basis_prep_circuit(state_symbols: str) -> QuantumCircuit:
    # Prepare multi-qubit X-basis state (e.g. '+-').
    n = len(state_symbols)
    qc = QuantumCircuit(n, name=f"Prep_{state_symbols}")
    
    for i, symbol in enumerate(reversed(state_symbols)):
        if symbol == '-':
            qc.x(i)
        qc.h(i)
    return qc
""" End State Prep """


"""Operator Utilities """
def get_composite_operator(labels: list[str]) -> Operator:
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

def get_circuit_operator(circuit: QuantumCircuit) -> Operator:
    # Convert any circuit to its unitary Operator
    return Operator.from_circuit(circuit)
"""End Operator Utilities"""


def create_zero_state(qr):
    """
    Function Constraints: Returns a circuit to prepare a |0>^n state.
    Inputs: qr (QuantumRegister)
    Outputs: QuantumCircuit
    """
    qc = QuantumCircuit(qr)
    # Qubits are |0> by default, so no gates needed.
    return qc

def create_plus_state(qr):
    """
    Function Constraints: Returns a circuit to prepare a |+>^n state.
    Inputs: qr (QuantumRegister)
    Outputs: QuantumCircuit
    """
    qc = QuantumCircuit(qr)
    qc.h(qr)
    return qc
