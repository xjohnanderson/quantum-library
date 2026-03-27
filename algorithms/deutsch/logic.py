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

def get_deutsch_jozsa_circuit(n_qubits: int, case: str) -> QuantumCircuit:
    # Function Constraints: Constructs the full Deutsch-Jozsa circuit.
    # Inputs: n_qubits (int), case (str)
    # Outputs: dj_circuit (QuantumCircuit)
    
    # Register sizes: n input bits, 1 auxiliary bit, n classical bits for measurement
    qc = QuantumCircuit(n_qubits + 1, n_qubits, name=f"DJ_{case}")

    # 1. State Preparation
    # Input qubits to |+>^n
    qc.h(range(n_qubits))
    # Auxiliary qubit to |->
    qc.x(n_qubits)
    qc.h(n_qubits)
    qc.barrier()

    # 2. Apply Oracle
    oracle = get_dj_oracle(n_qubits, case)
    qc.append(oracle, range(n_qubits + 1))
    qc.barrier()

    # 3. Interference: Apply H to input qubits
    qc.h(range(n_qubits))

    # 4. Measure
    qc.measure(range(n_qubits), range(n_qubits))

    return qc
