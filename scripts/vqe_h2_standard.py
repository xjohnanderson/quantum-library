# vqe_h2_standard.py
import numpy as np
from qiskit.primitives import Estimator               
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.transformers import FreezeCoreTransformer
from qiskit_nature.second_q.circuit.library import UCCSD
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from qiskit_nature.units import DistanceUnit

driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM,
)

problem = driver.run()
problem = FreezeCoreTransformer().transform(problem)

mapper = JordanWignerMapper()

# Chemically motivated ansatz (excellent for H2)
ansatz = UCCSD(
    num_spatial_orbitals=problem.num_spatial_orbitals,
    num_particles=problem.num_particles,
    qubit_mapper=mapper,
)

estimator = Estimator()          # exact, noiseless
optimizer = SLSQP(maxiter=500)

vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)

solver = GroundStateEigensolver(mapper, vqe)
result = solver.solve(problem)

print("=== Standard VQE (UCCSD) for H₂ ===")
print(f"Electronic ground state energy : {result.electronic_energies[0]:.10f} Hartree")
print(f"Total energy (with nuclear rep.): {result.total_energies[0]:.10f} Hartree")
print(f"Qubits                         : {ansatz.num_qubits}")
print(f"Parameters                     : {ansatz.num_parameters}")