# algorithms/shors/logic.py
# This script implements the Shor's Algorithm (Period Finding) circuit template.
# Inputs: n_count (int), n_target (int), modular_exp_gate (Gate)
# Outputs: qc (QuantumCircuit)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from factories.circuit_factory import get_iqft_circuit

def create_shor_circuit(n_count, n_target, modular_exp_gate):
    # Ensure we are working with a gate
    if isinstance(modular_exp_gate, QuantumCircuit):
        modular_exp_gate = modular_exp_gate.to_gate()

    qr_count = QuantumRegister(n_count, 'count')
    qr_target = QuantumRegister(n_target, 'target')
    cr = ClassicalRegister(n_count, 'c')
    qc = QuantumCircuit(qr_count, qr_target, cr)

    qc.h(qr_count)
    qc.x(qr_target[0])
    qc.barrier()

    # 2. Apply Controlled Modular Exponentiation Sequence
    # Each qubit j must apply U^(2^j)
    for q in range(n_count):
        # Create U^(2^q)
        u_power = modular_exp_gate.power(2**q)
        # Note: If modular_exp_gate is already controlled, 
        # you may need to decompose/re-control depending on your factory output.
        qc.append(u_power, [qr_count[q]] + qr_target[:])
    
    qc.barrier()

    # 3. Apply Inverse QFT
    iqft_circ = get_iqft_circuit(n_count)
    iqft_gate = iqft_circ.to_gate() if isinstance(iqft_circ, QuantumCircuit) else iqft_circ
    qc.append(iqft_gate, qr_count)

    qc.measure(qr_count, cr)
    return qc