# factories/oracle_factory.py

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import ZGate

"""Oracles"""
def get_bit_flip_oracle(case: str):
    # Deutsch oracle for bit-flip (constant/balanced cases)

    def _build_c0(qc): 
        pass                                 # f(x) = 0
    def _build_c1(qc): 
        qc.x(1)                              # f(x) = 1
    def _build_b0(qc): 
        qc.cx(0, 1)                          # f(x) = x
    def _build_b1(qc):
        qc.x(0)                              # f(x) = x ⊕ 1
        qc.cx(0, 1)
        qc.x(0)

    oracle_map = {
        'c0': _build_c0,
        'c1': _build_c1,
        'b0': _build_b0,
        'b1': _build_b1
    }

    if case not in oracle_map:
        raise ValueError(f"Unknown bit-flip case: {case}. "
                         f"Valid cases: {list(oracle_map.keys())}")

    qc = QuantumCircuit(2, name=f"U_bit_{case}")
    oracle_map[case](qc)
    return qc.to_gate()

def get_phase_flip_oracle(n_qubits: int, target_state: str):
    # Phase oracle that marks |target_state> with a -1 phase.
    qc = QuantumCircuit(n_qubits, name=f"U_phase_{target_state}")
    for i, bit in enumerate(reversed(target_state)):
        if bit == '0':
            qc.x(i)

    mcz = ZGate().control(n_qubits - 1)
    qc.append(mcz, range(n_qubits))

    for i, bit in enumerate(reversed(target_state)):
        if bit == '0':
            qc.x(i)
    return qc.to_gate()
"""End Oracles"""