# /algorithms/simons/logic.py
"""
Core logic for 3-qubit Simon's Algorithm.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from factories.circuit_factory import create_simon_oracle
from factories.basis_factory import create_zero_state, create_plus_state


def simons_algorithm_3qubit(s: str = "110") -> QuantumCircuit:
    """
    Returns a full 3-qubit Simon's algorithm circuit for a given secret string s.
    
    Parameters:
        s (str): Secret string of length 3 (e.g., "110"). Must not be "000".
    
    Returns:
        QuantumCircuit: Fully constructed Simon's circuit (6 qubits total)
    """
    if len(s) != 3 or s == "000":
        raise ValueError("Secret string must be length 3 and not '000'")

    n = 3
    # Quantum registers
    qr_input = QuantumRegister(n, 'q_input')
    qr_output = QuantumRegister(n, 'q_output')
    cr = ClassicalRegister(n, 'c')

    qc = QuantumCircuit(qr_input, qr_output, cr, name=f"Simons_s={s}")

    # Step 1: Initialize input register to |+⟩^n and output to |0⟩^n
    qc.compose(create_plus_state(qr_input), inplace=True)
    qc.compose(create_zero_state(qr_output), inplace=True)

    qc.barrier()

    # Step 2: Apply the Simon oracle
    oracle = create_simon_oracle(s)          # Note: your current factory version takes only s
    qc.append(oracle, qr_input[:] + qr_output[:])   # Use append instead of compose for Gate

    qc.barrier()

    # Step 3: Apply Hadamard gates to the input register again
    qc.h(qr_input)

    qc.barrier()

    # Step 4: Measure the input register
    qc.measure(qr_input, cr)

    return qc


def get_simon_circuit_example() -> QuantumCircuit:
    """Convenience function with a common secret string"""
    return simons_algorithm_3qubit(s="110")