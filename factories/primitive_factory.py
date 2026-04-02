# factories/primitive_factory.py

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator
import numpy as np


""" Gates """
def get_swap_gate(circuit, qubit_a, qubit_b):
    #Attaches a SWAP gate between two specified qubits.
    #Constructed via three CNOT gates: 
    #CNOT(a,b), CNOT(b,a), CNOT(a,b).
   
    circuit.cx(qubit_a, qubit_b)
    circuit.cx(qubit_b, qubit_a)
    circuit.cx(qubit_a, qubit_b)
    return circuit
""" End Gates """


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





