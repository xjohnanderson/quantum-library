# algorithms/shors/logic.py
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from factories import get_iqft_circuit

 
def create_shor_circuit(n_count: int, a: int, N: int):
    """Recommended Shor circuit — uses the fast matrix multiplier (any N)."""
    from factories.arithmetic_factory import get_modular_exponentiation_circuit_matrix

    mod_exp = get_modular_exponentiation_circuit_matrix(a, N, n_count)

    total_qubits = mod_exp.num_qubits
    qc = QuantumCircuit(total_qubits, n_count, name=f"Shor_N{N}_a{a}")

    qc.h(range(n_count))
    qc.compose(mod_exp, qubits=range(total_qubits), inplace=True)
    qc.barrier()

    iqft_circ = get_iqft_circuit(n_count)
    iqft_gate = iqft_circ.to_gate() if isinstance(iqft_circ, QuantumCircuit) else iqft_circ
    qc.append(iqft_gate, range(n_count))
    qc.measure(range(n_count), range(n_count))
    return qc


 
def create_shor_circuit_matrix_only(n_count: int, a: int, N: int):
    """Alias for the recommended matrix version."""
    return create_shor_circuit(n_count, a, N)


# Adder-based version (wide circuit)
def create_shor_circuit_adder(n_count: int, a: int, N: int):
    """Adder-based version (scalable but qubit-heavy)."""
    from factories.arithmetic_factory import get_modular_exponentiation_circuit_adder

    mod_exp = get_modular_exponentiation_circuit_adder(a, N, n_count)

    total_qubits = mod_exp.num_qubits
    qc = QuantumCircuit(total_qubits, n_count, name=f"Shor_N{N}_a{a}_adder")

    qc.h(range(n_count))
    qc.compose(mod_exp, qubits=range(total_qubits), inplace=True)
    qc.barrier()

    iqft_circ = get_iqft_circuit(n_count)
    iqft_gate = iqft_circ.to_gate() if isinstance(iqft_circ, QuantumCircuit) else iqft_circ
    qc.append(iqft_gate, range(n_count))
    qc.measure(range(n_count), range(n_count))
    return qc