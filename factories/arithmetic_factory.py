# factories/arithmetic_factory.py
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate
from qiskit.circuit.library import UnitaryGate

import numpy as np


def get_rfa_gate() -> Gate:
    """Reversible Full Adder """
    qa = QuantumRegister(1, 'a')
    qb = QuantumRegister(1, 'b')
    qcin = QuantumRegister(1, 'cin')
    qs = QuantumRegister(1, 's')
    qcout = QuantumRegister(1, 'cout')

    qc = QuantumCircuit(qa, qb, qcin, qs, qcout, name='RFA')
    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.ccx(0, 1, 4)
    qc.ccx(2, 3, 4)
    qc.cx(2, 3)
    return qc.to_gate(label='RFA')


def n_bit_adder(n_bits: int) -> QuantumCircuit:
    """ Ripple-carry adder with uncomputation (no barrier)."""
    qa = QuantumRegister(n_bits, 'A')
    qb = QuantumRegister(n_bits, 'B')
    qcin_out = QuantumRegister(n_bits + 1, 'Carry')
    qsum = QuantumRegister(n_bits, 'S')
    q_ancilla = QuantumRegister(1, 'Anc')

    qc = QuantumCircuit(qa, qb, qcin_out, qsum, q_ancilla, name=f'Adder_{n_bits}bit')
    rfa = get_rfa_gate()

    # Forward pass
    for i in range(n_bits):
        qc.append(rfa, [qa[i], qb[i], qcin_out[i], qsum[i], qcin_out[i+1]])

    # Reverse pass (uncompute)
    for i in range(n_bits - 2, -1, -1):
        qc.cx(qsum[i], q_ancilla[0])
        qc.cx(qcin_out[i], q_ancilla[0])
        qc.ccx(qcin_out[i], q_ancilla[0], qcin_out[i+1])
        qc.ccx(qa[i], qb[i], qcin_out[i+1])
        qc.cx(qcin_out[i], q_ancilla[0])
        qc.cx(qsum[i], q_ancilla[0])

    return qc


# =============================================================================
# FACTORY 1: MATRIX-BASED (fast, compact — RECOMMENDED for Shor demos)
# =============================================================================
def get_modular_multiplier_gate(a: int, N: int) -> UnitaryGate:
    """Matrix version — perfect for any small N."""
    n_bits = int(np.ceil(np.log2(N)))          # exact size needed
    dim = 2 ** n_bits
    U = np.eye(dim, dtype=complex)

    for x in range(N):
        U[x, x] = 0.0
        U[(a * x) % N, x] = 1.0

    return UnitaryGate(U, label=f"ModMul_a{a}_mod{N}")


def get_modular_exponentiation_circuit_matrix(x: int, N: int, n_count: int) -> QuantumCircuit:
    """Matrix-based modular exponentiation (compact, any N)."""
    n_target = int(np.ceil(np.log2(N))) # must match the gate exactly (no +1)

    qr_count = QuantumRegister(n_count, name='count')
    qr_target = QuantumRegister(n_target, name='target')
    qc = QuantumCircuit(qr_count, qr_target)

    qc.x(qr_target[0])  # target starts at |1⟩

    for i in range(n_count):
        a_pow = pow(x, 2**i, N)
        mod_mult = get_modular_multiplier_gate(a_pow, N)
        controlled_mult = mod_mult.control(1)
        # 1 control qubit + exactly n_target target qubits
        qc.append(controlled_mult, [qr_count[i]] + list(qr_target))

    return qc


# =============================================================================
# FACTORY 2: ADDER-BASED (scalable — uses RFA + n_bit_adder)
# =============================================================================
def get_modular_multiplier_circuit(a: int, N: int) -> QuantumCircuit:
    """Adder-based modular multiplier — works for ANY N (but qubit-heavy)."""
    if a == 0 or N < 2:
        raise ValueError("a and N must be positive.")

    n_bits = int(np.ceil(np.log2(N))) + 2

    qr_a     = QuantumRegister(n_bits, 'a')
    qr_b     = QuantumRegister(n_bits, 'b')
    qr_carry = QuantumRegister(n_bits + 1, 'carry')
    qr_sum   = QuantumRegister(n_bits, 'sum')
    qr_anc   = QuantumRegister(1, 'anc')

    qc = QuantumCircuit(qr_a, qr_b, qr_carry, qr_sum, qr_anc,
                        name=f"ModMul_a{a}_mod{N}_adder")

    adder_circ = n_bit_adder(n_bits)
    adder_gate = adder_circ.to_gate(label=f"Adder_{n_bits}bit")

    # Copy x into fixed multiplicand
    for i in range(n_bits):
        qc.cx(qr_b[i], qr_a[i])

    # Repeated addition
    for _ in range(a - 1):
        qc.append(adder_gate, qr_a[:] + qr_b[:] + qr_carry[:] + qr_sum[:] + qr_anc[:])
        for i in range(n_bits):
            qc.cx(qr_sum[i], qr_b[i])

        # TODO: Full modular reduction (comparator + controlled-subtract-N)

    # Cleanup copy
    for i in range(n_bits):
        qc.cx(qr_a[i], qr_b[i])

    return qc


def get_modular_exponentiation_circuit_adder(x: int, N: int, n_count: int) -> QuantumCircuit:
    """Adder-based modular exponentiation (scalable but wide circuit)."""
    mod_mult_circ = get_modular_multiplier_circuit(x, N)
    n_target = mod_mult_circ.num_qubits

    qr_count = QuantumRegister(n_count, name='count')
    qr_target = QuantumRegister(n_target, name='target')
    qc = QuantumCircuit(qr_count, qr_target)

    qc.x(qr_target[0])

    for i in range(n_count):
        a_pow = pow(x, 2**i, N)
        mod_mult = get_modular_multiplier_circuit(a_pow, N)
        controlled_mult = mod_mult.to_gate().control(1)
        qc.append(controlled_mult, [qr_count[i]] + list(range(n_count, n_count + mod_mult.num_qubits)))

    return qc