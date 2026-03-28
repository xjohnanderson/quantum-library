# factories/oracle_factory.py

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import ZGate
from qiskit.quantum_info import Operator
import numpy as np

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

"""Bernstein-Vazirani"""
def get_bernstein_vazirani_oracle(s: str) -> QuantumCircuit:
   
    #Creates the Bernstein-Vazirani oracle for a secret string s.
    
    #The oracle implements |x⟩|y⟩ → |x⟩|y ⊕ (s·x)⟩ where s·x is the dot product mod 2.
    
    n = len(s)
    if not all(bit in '01' for bit in s):
        raise ValueError("Secret string s must consist of '0's and '1's only.")
    
    qc = QuantumCircuit(n + 1, name=f"BV_oracle_s={s}")
    
    # Apply CNOT from each input qubit i to the target if s[i] == '1'
    for i, bit in enumerate(reversed(s)):   # reversed because Qiskit uses little-endian
        if bit == '1':
            qc.cx(i, n)                     # control = input qubit i, target = auxiliary
    
    return qc.to_gate()
"""End Bernstein-Vazirani"""


"""Deutsch-Jousza"""
def get_dj_oracle(n_qubits: int, case: str) -> QuantumCircuit:
    # Generates a Deutsch-Jozsa oracle.
    # Inputs: n_qubits (int), case (str: 'constant_0', 'constant_1', or 'balanced')
    # Outputs: dj_oracle (Gate)
    
    # We need n input qubits + 1 auxiliary qubit
    qc = QuantumCircuit(n_qubits + 1, name=f"DJ_Oracle_{case}")

    if case == 'constant_0':
        pass # f(x) = 0, do nothing
    elif case == 'constant_1':
        qc.x(n_qubits) # f(x) = 1, flip auxiliary qubit
    elif case == 'balanced':
        # Simple balanced oracle: XOR sum of bits. 
        # Flip auxiliary if an odd number of input bits are 1.
        for i in range(n_qubits):
            qc.cx(i, n_qubits)
    else:
        raise ValueError("Case must be 'constant_0', 'constant_1', or 'balanced'")

    return qc.to_gate()


"""End Deutsch-Jousza"""


"""Simon's Algorithm"""

def create_simon_oracle(s: str) -> QuantumCircuit:
    """
    Creates a valid 2-to-1 Simon oracle where f(x) = f(x ⊕ s).
    """
    n = len(s)
    qc = QuantumCircuit(n + n, name=f"SimonOracle_s={s}")
    
    # Qiskit little-endian: s_bits[0] is the rightmost bit (LSB)
    s_bits = [int(bit) for bit in reversed(s)]
    
    # Find the first index 'k' where s_k == 1 to act as the reference/shift bit
    k = -1
    for i, bit in enumerate(s_bits):
        if bit == 1:
            k = i
            break

    # If s is "000", the oracle is just a 1-to-1 identity mapping
    if k == -1:
        for i in range(n):
            qc.cx(i, n + i)
        return qc.to_gate()

    # 2-to-1 Mapping Logic:
    # We ensure that flipping the bits of s in the input results in the same output.
    for i in range(n):
        if s_bits[i] == 1:
            if i != k:
                # Output bit i becomes the XOR of input bit i and reference bit k
                # f(x)_i = x_i ⊕ x_k
                qc.cx(k, n + i)
                qc.cx(i, n + i)
            # If i == k, we leave the output bit n+k as |0>. 
            # This ensures f(x) = f(x ⊕ s) because both inputs map to 0 at this index.
        else:
            # 1-to-1 mapping for bits where s_i == 0
            qc.cx(i, n + i)

    return qc.to_gate()
"""End Simon's Algorithm"""


