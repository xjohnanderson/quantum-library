import unittest
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator, Statevector
from factories.primitive_factory import (
    get_swap_gate,
    attach_bell_state_prep,
    attach_bell_measurement,
    get_x_basis_prep_circuit,
    create_zero_state,
    create_plus_state,
    get_composite_operator,
    get_evolution_circuit,
    get_circuit_operator
)

class TestPrimitiveFactory(unittest.TestCase):
    def test_create_zero_state(self):
        qr = QuantumRegister(2)
        qc = create_zero_state(qr)
        self.assertEqual(qc.size(), 0)
        self.assertEqual(qc.width(), 2)

    def test_create_plus_state(self):
        n = 3
        qr = QuantumRegister(n)
        qc = create_plus_state(qr)
        self.assertEqual(qc.size(), n)
        self.assertEqual(qc.width(), n)
        for instruction in qc.data:
            self.assertEqual(instruction.operation.name, 'h')

    def test_get_swap_gate(self):
        qc = QuantumCircuit(2)
        get_swap_gate(qc, 0, 1)
        # Should have 3 CX gates
        self.assertEqual(qc.size(), 3)
        for instruction in qc.data:
            self.assertEqual(instruction.operation.name, 'cx')
        
        # Verify it actually swaps states
        # |10> -> |01>
        initial_state = Statevector.from_label('10')
        final_state = initial_state.evolve(qc)
        self.assertTrue(final_state.equiv(Statevector.from_label('01')))

    def test_attach_bell_state_prep(self):
        qc = QuantumCircuit(2)
        attach_bell_state_prep(qc, 0, 1)
        self.assertEqual(qc.size(), 2)
        self.assertEqual(qc.data[0].operation.name, 'h')
        self.assertEqual(qc.data[1].operation.name, 'cx')
        
        # Verify it creates Phi+ = (|00> + |11>) / sqrt(2)
        final_state = Statevector.from_instruction(qc)
        expected_state = Statevector([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
        self.assertTrue(final_state.equiv(expected_state))

    def test_attach_bell_measurement(self):
        qc = QuantumCircuit(2)
        attach_bell_measurement(qc, 0, 1)
        self.assertEqual(qc.size(), 2)
        self.assertEqual(qc.data[0].operation.name, 'cx')
        self.assertEqual(qc.data[1].operation.name, 'h')

    def test_get_x_basis_prep_circuit(self):
        # Test '+-'
        # '+' is H|0>
        # '-' is H|1> = H X |0>
        qc = get_x_basis_prep_circuit('+-')
        # symbols are reversed in loop: '-' at index 0, '+' at index 1
        # '-' -> X then H on i=0
        # '+' -> H on i=1
        # Total 3 gates
        self.assertEqual(qc.size(), 3)
        
        state = Statevector.from_instruction(qc)
        # '+-' in Qiskit ordering is |-> tensor |+>
        # |+> = [1, 1]/sqrt(2)
        # |-> = [1, -1]/sqrt(2)
        plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
        minus = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])
        expected = plus.tensor(minus) 
        self.assertTrue(state.equiv(expected))

    def test_get_composite_operator(self):
        # X tensor Z
        op = get_composite_operator(['X', 'Z'])
        expected = Operator.from_label('X').tensor(Operator.from_label('Z'))
        self.assertTrue(op.equiv(expected))

    def test_get_evolution_circuit(self):
        qc = get_evolution_circuit()
        self.assertEqual(qc.width(), 1)
        # H-T-H-S-Y
        gate_names = [inst.operation.name for inst in qc.data]
        self.assertEqual(gate_names, ['h', 't', 'h', 's', 'y'])

    def test_get_circuit_operator(self):
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.x(0)
        op = get_circuit_operator(qc)
        expected = Operator.from_label('X') @ Operator.from_label('H')
        self.assertTrue(op.equiv(expected))

if __name__ == "__main__":
    unittest.main()
