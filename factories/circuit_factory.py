# factories/circuit_factory.py
# Reusable circuit components, gates, oracles, and circuit templates.

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import ZGate, QFT
from qiskit.quantum_info import Operator
from utils.math_ops import get_mod_inv
import numpy as np

"""Bell Protocol Helpers """
def attach_bell_state_prep(qc, q0, q1):
    # Appends H and CX to create a Phi+ |Φ+⟩ Bell state.
    qc.h(q0)
    qc.cx(q0, q1)
    return qc

def attach_bell_measurement(qc, q_control, q_target):
    # Appends CX + H for Bell-basis measurement
    qc.cx(q_control, q_target)
    qc.h(q_control)
    return qc
"""End Bell Protocol Helpers """

"""CHSH Circuit"""
def get_chsh_circuit(x: int, y: int) -> QuantumCircuit:
    # Constructs a 2-qubit CHSH circuit for measurement settings (x, y)

    if x not in (0, 1) or y not in (0, 1):
        raise ValueError("x and y must be 0 or 1.")
    
    qc = QuantumCircuit(2, 2, name=f"CHSH_x{x}_y{y}")
    
    # 1. Prepare Shared Entanglement (Phi+)
    attach_bell_state_prep(qc, 0, 1)
    qc.barrier()
    
    # 2. Alice's Basis Rotation (x=0: Z-basis, x=1: X-basis)
    if x == 1:
        qc.ry(-np.pi / 2, 0)
        
    # 3. Bob's Basis Rotation (y=0: W1, y=1: W2)
    # Angles are pi/8 and -pi/8 relative to Alice's bases.
    theta_b = -np.pi / 4 if y == 0 else np.pi / 4
    qc.ry(theta_b, 1)
        
    qc.measure([0, 1], [0, 1])
    return qc
"""End CHSH Circuit"""



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


"""Grover"""
def get_diffuser(n_qubits: int):
    """Constructs the Grover diffusion operator (H(2|0⟩⟨0|-I)H).

    This is the standard reflection-about-the-mean operator used in Grover's algorithm.
    """
    qc = QuantumCircuit(n_qubits, name="Diffuser")

    # 1. Enter Hadamard basis
    qc.h(range(n_qubits))

    # 2. Phase flip on |00...0> using the phase oracle
    zero_mark = '0' * n_qubits
    qc.append(get_phase_flip_oracle(n_qubits, zero_mark), range(n_qubits))

    # 3. Exit Hadamard basis
    qc.h(range(n_qubits))

    return qc.to_gate()
"""End Grover"""

"""Custom Gates"""
def get_rfa_gate():
    # Function Constraints: Defines a Reversible Full Adder (RFA).
    # Inputs: None
    # Outputs: rfa_gate (Gate)
    
    qa = QuantumRegister(1, 'A')
    qb = QuantumRegister(1, 'B')
    qcin = QuantumRegister(1, 'Cin')
    qs = QuantumRegister(1, 'S')
    qcout = QuantumRegister(1, 'Cout')
    
    qc = QuantumCircuit(qa, qb, qcin, qs, qcout, name='RFA')
    
    # Logic: S = A ^ B ^ Cin | Cout = (A & B) | (Cin & (A ^ B))
    qc.cx(0, 3)     # A to Sum
    qc.cx(1, 3)     # B to Sum
    qc.ccx(0, 1, 4) # A & B to Cout
    qc.ccx(2, 3, 4) # Cin & Sum_intermediate to Cout
    qc.cx(2, 3)     # Final Sum
    
    return qc.to_gate(label='RFA')


def get_modular_multiplier_gate(a, N):
    # Function Constraints: Implements the unitary permutation |x> -> |a*x mod N>.
    n_bits = int(np.ceil(np.log2(N)))
    U = np.zeros((2**n_bits, 2**n_bits))
    
    for x in range(2**n_bits):
        if x < N:
            U[(a * x) % N, x] = 1
        else:
            U[x, x] = 1 
            
    return Operator(U)
"""End Custom Gates"""


""" State Prep """
def get_x_basis_prep_circuit(state_symbols):
    # Function Constraints: Returns a circuit to prepare a multi-qubit X-basis state.
    # Inputs: state_symbols (str e.g., "+-")
    # Outputs: QuantumCircuit
    n = len(state_symbols)
    qc = QuantumCircuit(n, name=f"Prep_{state_symbols}")
    
    for i, symbol in enumerate(reversed(state_symbols)):
        if symbol == '-':
            qc.x(i)
        qc.h(i)
    return qc
""" End State Prep """


"""Operator Utilities """
def get_composite_operator(labels: list):
    # Create multi-qubit Operator from list of single-qubit labels.
    op = Operator.from_label(labels[0])
    for label in labels[1:]:
        op = op.tensor(Operator.from_label(label))
    return op

def get_evolution_circuit() -> QuantumCircuit:
    # Example custom single-qubit evolution: H-T-H-S-Y
    qc = QuantumCircuit(1, name="CustomEvolution")
    qc.h(0)
    qc.t(0)
    qc.h(0)
    qc.s(0)
    qc.y(0)
    return qc

def get_circuit_operator(circuit: QuantumCircuit):
    # Convert any circuit to its unitary Operator
    return Operator.from_circuit(circuit)
"""End Operator Utilities"""



"""Fourier Transform"""
def get_iqft_circuit(n_qubits: int, do_swaps: bool = True) -> QuantumCircuit:
    # Returns the Inverse Quantum Fourier Transform (IQFT) circuit.

    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1.")

    iqft = QFT(
        num_qubits=n_qubits,
        approximation_degree=0,
        do_swaps=do_swaps,
        inverse=True,
        name="IQFT"
    )
    # Return as circuit (most convenient for appending)
    return iqft


def get_qft_circuit(n_qubits: int, do_swaps: bool = True) -> QuantumCircuit:
    # Returns the (forward) Quantum Fourier Transform circuit
    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1.")

    qft = QFT(
        num_qubits=n_qubits,
        approximation_degree=0,
        do_swaps=do_swaps,
        inverse=False,
        name="QFT"
    )
    return qft
"""End Fourier Transform"""



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



def get_bernstein_vazirani_circuit(s: str) -> QuantumCircuit:
     
    #Full Bernstein-Vazirani circuit for secret string s.
    
    #Returns a circuit that should measure the secret string s with probability 1.
     
    n = len(s)
    qc = QuantumCircuit(n + 1, n, name=f"BernsteinVazirani_s={s}")
    
    # 1. Initialize input register to |+...+⟩ and auxiliary to |-> 
    qc.h(range(n))           # superposition on input qubits
    qc.x(n)                  # auxiliary to |1⟩
    qc.h(n)                  # auxiliary to |-> 
    qc.barrier()
    
    # 2. Apply the oracle
    oracle = get_bernstein_vazirani_oracle(s)
    qc.append(oracle, range(n + 1))
    qc.barrier()
    
    # 3. Apply Hadamard again on input register (Fourier transform back)
    qc.h(range(n))
    
    # 4. Measure input register (auxiliary qubit is not measured)
    qc.measure(range(n), range(n))
    
    return qc
"""End Bernstein-Vazirani"""