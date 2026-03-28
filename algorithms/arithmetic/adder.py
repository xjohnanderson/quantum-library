# algorithms/arithmetic/adder.py
# Function Constraints: Implements a Ripple Carry Adder using RFA gates.
# Inputs: n (int) - bit width.
# Outputs: qc (QuantumCircuit) - ~4n+2 logical qubits, high T-depth.

from qiskit import QuantumCircuit, QuantumRegister
from factories.primitive_factory import get_rfa_gate 

def n_bit_adder(n_bits):
    # Function Constraints: Constructs an N-bit ripple-carry adder with uncomputation.
    # Inputs: n_bits (int)
    # Outputs: adder_circuit (QuantumCircuit)
    
    qa = QuantumRegister(n_bits, 'A')
    qb = QuantumRegister(n_bits, 'B')
    qcin_out = QuantumRegister(n_bits + 1, 'Carry')
    qsum = QuantumRegister(n_bits, 'S')
    q_ancilla = QuantumRegister(1, 'Anc')

    qc = QuantumCircuit(qa, qb, qcin_out, qsum, q_ancilla, name=f'Adder_{n_bits}bit')
    rfa = get_rfa_gate()

    # 1. Forward Pass: Compute Sum and Carry
    for i in range(n_bits):
        qc.append(rfa, [qa[i], qb[i], qcin_out[i], qsum[i], qcin_out[i+1]])

    qc.barrier(label='Uncompute')

    # 2. Reverse Pass: Uncompute intermediate carries to prevent entanglement
    for i in range(n_bits - 2, -1, -1):
        # Mirroring the RFA logic to reset Carry bits
        qc.cx(qsum[i], q_ancilla[0])
        qc.cx(qcin_out[i], q_ancilla[0])
        qc.ccx(qcin_out[i], q_ancilla[0], qcin_out[i+1])
        qc.ccx(qa[i], qb[i], qcin_out[i+1])
        qc.cx(qcin_out[i], q_ancilla[0])
        qc.cx(qsum[i], q_ancilla[0])

    return qc