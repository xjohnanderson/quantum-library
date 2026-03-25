# factories/state_factory.py
# Script: Provides high-level methods to evolve basis states into specific oracle-transformed states
#         and other specially prepared states (W-state, GHZ, etc.).

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

from factories.basis_factory import X_BASIS


def _evolve_x_basis(label: str, gate_type: str) -> Statevector:
    # Internal helper: Evolves an X-basis state using a specified 2-qubit gate. 
    if label not in X_BASIS:
        raise ValueError(f"Label '{label}' not found in X_BASIS.")
        
    initial_state = X_BASIS[label]
    qc = QuantumCircuit(2)
    
    gate_map = {
        'cx': qc.cx,
        'cz': qc.cz,
        'cy': qc.cy
    }
    
    if gate_type in gate_map:
        gate_map[gate_type](0, 1)   # control=0, target=1
    else:
        raise NotImplementedError(f"Gate type '{gate_type}' is not supported.")
        
    return initial_state.evolve(qc)


def get_cz_statevector(label: str) -> Statevector:
    # Evolves X-basis state via a CZ gate (symmetric phase flip). 
    return _evolve_x_basis(label, 'cz')


def get_cx_statevector(label: str) -> Statevector:
    # Evolves X-basis state via a CX gate (directional phase kickback). 
    return _evolve_x_basis(label, 'cx')


def get_cy_statevector(label: str) -> Statevector:
    # Evolves X-basis state via a CY gate (complex phase rotation). 
    return _evolve_x_basis(label, 'cy')