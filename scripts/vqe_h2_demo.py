# scripts/run_vqe_h2_demo.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_nature.second_q.mappers import JordanWignerMapper

 
from factories import (
    create_h2_problem,
    create_uccsd_ansatz,
    create_hardware_efficient_ansatz,
)

print("🚀 Running VQE for H₂ molecule...\n")

# 1. Create the molecular problem
problem = create_h2_problem(bond_length=0.735)

# 2. Mapper + Ansatz
mapper = JordanWignerMapper()

# === CHOOSE ONE (uncomment the one you want) ===
# A) UCCSD — chemically accurate (default)
ansatz = create_uccsd_ansatz(problem, mapper)

# B) Your hardware-efficient ansatz with factories (for comparison)
# ansatz = create_hardware_efficient_ansatz(
#     num_qubits=4,
#     reps=4,
#     initial_state="bell"       # options: "plus", "bell", "x_++", "x_+-", None
# )

print(f"Ansatz type : {ansatz.name}")
print(f"Qubits      : {ansatz.num_qubits}")
print(f"Parameters  : {ansatz.num_parameters}\n")

# 3. Run VQE
vqe = VQE(
    estimator=Estimator(),
    ansatz=ansatz,
    optimizer=SLSQP(maxiter=1000),
)

solver = GroundStateEigensolver(mapper, vqe)
result = solver.solve(problem)

# 4. Results
print("=== VQE Results for H₂ (STO-3G) ===")
print(f"Electronic ground state energy : {result.electronic_energies[0]:.10f} Hartree")
print(f"Total ground state energy      : {result.total_energies[0]:.10f} Hartree")
print(f"Qubits used                    : {ansatz.num_qubits}")
print(f"Parameters                     : {ansatz.num_parameters}")

raw = result.raw_result
print(f"Optimizer evaluations          : {getattr(raw, 'optimizer_evals', 'N/A')}")