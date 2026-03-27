from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate

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