# algorithms/teleportation/logic.py
# path_to_file: algorithms/teleportation/logic.py
# This script constructs the 3-qubit Quantum Teleportation protocol circuit.

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from utils.constants import ALICE_SOURCE_INDEX, ALICE_EBIT_INDEX, BOB_EBIT_INDEX

def get_teleportation_circuit(simulation_mode=False, name="teleportation_protocol"):
    # Function Constraints: Constructs a 3-qubit teleportation pipeline.
    # simulation_mode (bool): If True, skips measurements/if_tests for Statevector analysis.
    
    qr = QuantumRegister(3, name="q")
    
    if simulation_mode:
        # No classical registers needed for pure statevector math
        qc = QuantumCircuit(qr, name=name)
    else:
        cr_ebit = ClassicalRegister(1, name="c_ebit")
        cr_src = ClassicalRegister(1, name="c_src")
        qc = QuantumCircuit(qr, cr_ebit, cr_src, name=name)

    # 1. Resource Preparation: Bell State |phi+>
    qc.h(ALICE_EBIT_INDEX)
    qc.cx(ALICE_EBIT_INDEX, BOB_EBIT_INDEX)
    qc.barrier()

    # 2. Alice's Operations: Bell Measurement Basis Change
    qc.cx(ALICE_SOURCE_INDEX, ALICE_EBIT_INDEX)
    qc.h(ALICE_SOURCE_INDEX)
    qc.barrier()

    # 3. Conditional Logic: Skip if in simulation_mode
    if not simulation_mode:
        qc.measure(ALICE_EBIT_INDEX, cr_ebit)
        qc.measure(ALICE_SOURCE_INDEX, cr_src)
        qc.barrier()

        with qc.if_test((cr_ebit, 1)):
            qc.x(BOB_EBIT_INDEX)
        with qc.if_test((cr_src, 1)):
            qc.z(BOB_EBIT_INDEX)
    
    return qc