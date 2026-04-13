import unittest
from qiskit_nature.second_q.problems import ElectronicStructureProblem
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit.circuit import QuantumCircuit
from factories.vqe_factory import (
    create_h2_problem,
    create_uccsd_ansatz,
    create_hardware_efficient_ansatz
)

class TestVQEFactory(unittest.TestCase):
    def test_create_h2_problem(self):
        # This might be slow but it's small (H2, sto3g)
        problem = create_h2_problem(bond_length=0.735)
        self.assertIsInstance(problem, ElectronicStructureProblem)
        # H2 in sto3g has 2 atoms, 2 electrons, 4 spin-orbitals (2 spatial)
        # If freeze_core=True (default), it's the same for H2 as there are no core electrons.
        self.assertEqual(problem.num_particles, (1, 1)) # 1 alpha, 1 beta
        self.assertEqual(problem.num_spatial_orbitals, 2)

    def test_create_uccsd_ansatz(self):
        problem = create_h2_problem(bond_length=0.735)
        mapper = JordanWignerMapper()
        ansatz = create_uccsd_ansatz(problem, mapper)
        self.assertIsInstance(ansatz, QuantumCircuit)
        self.assertEqual(ansatz.name, "UCCSD")
        # 4 spin orbitals -> 4 qubits with JordanWigner
        self.assertEqual(ansatz.num_qubits, 4)

    def test_create_hardware_efficient_ansatz_default(self):
        ansatz = create_hardware_efficient_ansatz(num_qubits=2, reps=1)
        self.assertIsInstance(ansatz, QuantumCircuit)
        self.assertEqual(ansatz.num_qubits, 2)
        # EfficientSU2 with reps=1 has 2*(reps+1) = 4 RY, 4 RZ gates (if linear and all rotations)
        # Actually EfficientSU2 default rotations are 'ry', 'rz'
        self.assertEqual(ansatz.num_parameters, 8)

    def test_create_hardware_efficient_ansatz_plus(self):
        ansatz = create_hardware_efficient_ansatz(num_qubits=2, reps=1, initial_state_label="plus")
        # Should have 2 H gates at the beginning
        # Gate names: h, h, then EfficientSU2 gates
        gate_names = [inst.operation.name for inst in ansatz.data]
        self.assertIn('h', gate_names)
        self.assertEqual(gate_names.count('h'), 2)

    def test_create_hardware_efficient_ansatz_bell(self):
        ansatz = create_hardware_efficient_ansatz(num_qubits=2, reps=1, initial_state_label="bell")
        gate_names = [inst.operation.name for inst in ansatz.data]
        self.assertIn('h', gate_names)
        self.assertIn('cx', gate_names)

    def test_create_hardware_efficient_ansatz_x_basis(self):
        ansatz = create_hardware_efficient_ansatz(num_qubits=2, reps=1, initial_state_label="x_+-")
        # x_+- -> Q0=+, Q1=-
        # Q0: H
        # Q1: X, H
        gate_names = [inst.operation.name for inst in ansatz.data]
        self.assertEqual(gate_names.count('h'), 2)
        self.assertEqual(gate_names.count('x'), 1)

if __name__ == "__main__":
    unittest.main()
