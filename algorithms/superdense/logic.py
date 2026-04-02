# algorithms/superdense/logic.py
# Script: Constructs the Superdense Coding protocol circuit.

from qiskit import QuantumCircuit

def get_superdense_circuit(bit_c: str, bit_d: str) -> QuantumCircuit:
    # Function Constraints: Alice encodes two bits into one qubit of a Bell pair.
    # Inputs: bit_c (str), bit_d (str) '0' or '1'
    # Outputs: qc (QuantumCircuit)
    qc = QuantumCircuit(2, name=f"Superdense_{bit_c}{bit_d}")

    # 1. Prepare Bell state |phi+> (Can also use factories.protocol_factory)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # 2. Alice's Encoding (Only operates on qubit 0)
    if bit_d == "1":
        qc.z(0)
    if bit_c == "1":
        qc.x(0)
    qc.barrier()

    # 3. Bob's Decoding (Bell basis measurement)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure_all()
    
    return qc