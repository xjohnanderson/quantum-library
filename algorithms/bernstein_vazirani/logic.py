from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from factories.oracle_factory import get_bernstein_vazirani_oracle 
from analysis.kickback import verify_kickback, report_phase_diagnostics
from utils.visualization import show_state

def get_bernstein_vazirani_circuit(s: str, include_measurement: bool = True) -> QuantumCircuit:
    """Constructs the BV circuit. Set include_measurement=False for statevector analysis."""
    n = len(s)
    qc = QuantumCircuit(n + 1, n if include_measurement else 0, name=f"BV_{s}")
    
    # 1. State Prep: |+...+> |->
    qc.h(range(n))
    qc.x(n)
    qc.h(n)
    qc.barrier()
    
    # 2. Oracle Application
    oracle = get_bernstein_vazirani_oracle(s)
    qc.compose(oracle, range(n + 1), inplace=True)
    
    # ←←← THIS IS THE KEY FIX
    qc = qc.decompose()          # expands the custom oracle gate into CX gates
    
    qc.barrier()
    
    if include_measurement:
        qc.h(range(n))
        qc.measure(range(n), range(n))
    
    return qc

def analyze_phase_kickback(s: str = "101"):
    """Isolates the oracle's effect on the statevector to verify kickback."""
    n = len(s)
    
    # Pre-oracle state: H^n |0> \otimes H|1>
    qc_pre = QuantumCircuit(n + 1)
    qc_pre.h(range(n))
    qc_pre.x(n)
    qc_pre.h(n)
    pre_state = Statevector.from_instruction(qc_pre)
    
    # Evolve through oracle
    oracle = get_bernstein_vazirani_oracle(s)
    post_state = pre_state.evolve(oracle)
    
    # Analysis
    kickback_detected, global_phase = verify_kickback(pre_state, post_state)
    report_phase_diagnostics(kickback_detected, global_phase)
    
    if n <= 4:
        show_state(post_state, label=f"Post-oracle Statevector (s = {s})")



def run_bernstein_vazirani(s: str, simulator=None):
    """Executes the full algorithm and returns measurement counts."""
    sim = simulator or AerSimulator()
    qc = get_bernstein_vazirani_circuit(s)
    
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    measured = max(counts, key=counts.get)
    
    print(f"Secret: {s} | Measured: {measured} | Match: {measured == s}")
    return qc, counts