# factories/algorithm_factory.py

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


"""Deutsch-Jousza"""

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

"""End Deutsch-Jousza"""


"""CHSH Game"""
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
"""End CHSH Game"""