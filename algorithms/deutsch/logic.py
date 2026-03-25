# algorithms/deutsch/logic.py
# This script implements the Deutsch Algorithm template.

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_deutsch_circuit(oracle_gate):
    # Function Constraints: Wraps an oracle to determine if it's constant or balanced.
    # Inputs: oracle_gate (QuantumCircuit or Gate)
    # Outputs: qc (QuantumCircuit)
    
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(qr, cr)

    # 1. Initialize auxiliary qubit to |-> for phase kickback
    qc.x(1)
    qc.h(1)

    # 2. Prepare input qubit in superposition |+>
    qc.h(0)
    qc.barrier()

    # 3. Apply the oracle
    qc.append(oracle_gate, [0, 1])
    qc.barrier()

    # 4. Measure input in X-basis (H then Z-measure)
    qc.h(0)
    qc.measure(0, 0)

    return qc