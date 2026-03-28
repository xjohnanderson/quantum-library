# algorithms/bernstein_vazirani/logic.py

from qiskit import QuantumCircuit
from factories.oracle_factory import get_bernstein_vazirani_oracle 
from factories.basis_factory import get_2qubit_z_basis   
from analysis.kickback import verify_kickback, report_phase_diagnostics
from qiskit.quantum_info import Statevector


def analyze_phase_kickback(secret: str = "101"):
    """Demonstrate phase kickback using your kickback analysis module."""
    print(f"\n=== Phase Kickback Analysis for s = '{secret}' ===")
    
    n = len(secret)
    
    # Prepare initial state: |+...+⟩ |-> 
    qc_init = QuantumCircuit(n + 1)
    qc_init.h(range(n))      # input register in superposition
    qc_init.x(n)             # auxiliary to |1>
    qc_init.h(n)             # auxiliary to |-> 
    pre_state = Statevector.from_instruction(qc_init)
    
    # Apply oracle
    oracle = get_bernstein_vazirani_oracle(secret)
    post_state = pre_state.evolve(oracle)
    
    # Use your existing analysis tool
    kickback_detected, global_phase = verify_kickback(pre_state, post_state)
    report_phase_diagnostics(kickback_detected, global_phase)
    
    if n <= 4:
        print("\nPost-oracle statevector (phases on input register encode the secret):")
        print(post_state)

def run_bernstein_vazirani(s: str, simulator=None):
    """Run Bernstein-Vazirani for secret string s."""
    if simulator is None:
        from qiskit_aer import AerSimulator
        simulator = AerSimulator()
    
    qc = get_bernstein_vazirani_circuit(s)
    
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    
    # The most probable (ideally only) outcome should be the secret string
    measured = max(counts, key=counts.get)
    
    print(f"Secret string:         {s}")
    print(f"Measured string:       {measured}")
    print(f"Success:               {measured == s}")
    print(f"Counts:                {counts}")
    
    return qc, counts


def demonstrate_phase_kickback(s: str = "101"):
    """Show phase kickback effect in Bernstein-Vazirani."""
    print(f"\n=== Phase Kickback Demo for s = {s} ===\n")
    
    n = len(s)
    # Initial state before oracle: |+...+⟩|-> 
    qc_init = QuantumCircuit(n + 1)
    qc_init.h(range(n))
    qc_init.x(n)
    qc_init.h(n)
    pre_state = Statevector.from_instruction(qc_init)
    
    # After oracle
    oracle = get_bernstein_vazirani_oracle(s)
    post_state = pre_state.evolve(oracle)
    
    kickback_detected, global_phase = verify_kickback(pre_state, post_state)
    report_phase_diagnostics(kickback_detected, global_phase)
    
    # Optional: show that the input register acquired phases corresponding to s
    print("Post-oracle state (input register phases encode the secret):")
    print(post_state)



 

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
 