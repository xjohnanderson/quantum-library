# factories/basis_factory.py
# Pure basis states and common statevectors.

from qiskit.quantum_info import Statevector
import numpy as np


def get_w_state() -> Statevector:
    # Returns the 3-qubit W-state: (|001> + |010> + |100>) / sqrt(3) 
    data = np.array([0, 1, 1, 0, 1, 0, 0, 0], dtype=complex) / np.sqrt(3)
    return Statevector(data)

def get_2qubit_z_basis():
    # Computational (Z) basis for 2 qubits
    return {f"{i:02b}": Statevector.from_label(f"{i:02b}") for i in range(4)}

def get_2qubit_x_basis():
    # X-basis states using tensor products.
    plus = Statevector.from_label('+')
    minus = Statevector.from_label('-')
    map_states = {'+': plus, '-': minus}
    
    labels = ['++', '+-', '-+', '--']
    return {label: map_states[label[1]] ^ map_states[label[0]] for label in labels}

def get_2qubit_y_basis():
    # Y-basis states using tensor products
    r = Statevector.from_label('r')
    l = Statevector.from_label('l')
    map_states = {'r': r, 'l': l}
    
    labels = ['rr', 'rl', 'lr', 'll']
    return {label: map_states[label[1]] ^ map_states[label[0]] for label in labels}

def get_bell_basis():
    # Four maximally entangled Bell states
    z = get_2qubit_z_basis()
    return {
        'phi+': (z['00'] + z['11']) / np.sqrt(2),
        'phi-': (z['00'] - z['11']) / np.sqrt(2),
        'psi+': (z['01'] + z['10']) / np.sqrt(2),
        'psi-': (z['01'] - z['10']) / np.sqrt(2)
    }


def get_3qubit_z_basis():
    """Computational (Z) basis for 3 qubits"""
    return {f"{i:03b}": Statevector.from_label(f"{i:03b}") for i in range(8)}

def get_ghz_basis() -> dict[str, Statevector]:
    """
    Returns the 3-qubit GHZ basis (also known as the GHZ-type entangled basis).
    
    The standard GHZ state is |GHZ⟩ = (|000⟩ + |111⟩)/√2
    We also include the three other orthogonal states that complete the basis:
        |GHZ⟩, |GHZ'⟩ = (|000⟩ - |111⟩)/√2,
        |GHZ''⟩ = (|001⟩ + |110⟩)/√2,
        |GHZ'''⟩ = (|001⟩ - |110⟩)/√2  (and cyclic permutations)
    """
    z = get_3qubit_z_basis()          
    
    return {
        'ghz+':  (z['000'] + z['111']) / np.sqrt(2),   # standard GHZ
        'ghz-':  (z['000'] - z['111']) / np.sqrt(2),
        'ghz1+': (z['001'] + z['110']) / np.sqrt(2),
        'ghz1-': (z['001'] - z['110']) / np.sqrt(2),
        'ghz2+': (z['010'] + z['101']) / np.sqrt(2),
        'ghz2-': (z['010'] - z['101']) / np.sqrt(2),
        'ghz3+': (z['100'] + z['011']) / np.sqrt(2),
        'ghz3-': (z['100'] - z['011']) / np.sqrt(2),
    }






# Exported Constants
Z_BASIS = get_2qubit_z_basis()
X_BASIS = get_2qubit_x_basis()
Y_BASIS = get_2qubit_y_basis()
BELL_BASIS = get_bell_basis()
GHZ_BASIS  = get_ghz_basis()   