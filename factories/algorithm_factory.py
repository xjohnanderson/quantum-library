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
