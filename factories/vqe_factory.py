# factories/vqe_factory.py
"""VQE-specific factories for molecule and ansatz creation."""

from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import FreezeCoreTransformer
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock
from qiskit.circuit.library import EfficientSU2
from qiskit import QuantumCircuit, QuantumRegister
from qiskit_nature.second_q.mappers import QubitMapper
from qiskit_nature.second_q.problems import ElectronicStructureProblem

# Reuse existing factories
from .primitive_factory import attach_bell_state_prep, get_x_basis_prep_circuit, create_plus_state


def create_h2_problem(bond_length: float = 0.735, basis: str = "sto3g", freeze_core: bool = True) -> ElectronicStructureProblem:
    """
    Create ElectronicStructureProblem for H₂.
    
    Inputs:
        bond_length (float): Distance between H atoms in Angstroms.
        basis (str): Atomic basis set (default sto3g).
        freeze_core (bool): Whether to apply FreezeCoreTransformer.
    Outputs:
        problem (ElectronicStructureProblem): The generated molecular problem.
    """
    atom_str = f"H 0 0 0; H 0 0 {bond_length}"
    driver = PySCFDriver(
        atom=atom_str,
        basis=basis,
        charge=0,
        spin=0,
        unit=DistanceUnit.ANGSTROM,
    )
    problem = driver.run()
    if freeze_core:
        problem = FreezeCoreTransformer().transform(problem)
    return problem


def create_uccsd_ansatz(problem: ElectronicStructureProblem, mapper: QubitMapper) -> QuantumCircuit:
    """
    Chemically motivated UCCSD ansatz with Hartree-Fock initial state.
    
    Inputs:
        problem (ElectronicStructureProblem): The molecular structure data.
        mapper (QubitMapper): The fermion-to-qubit mapping strategy.
    Outputs:
        circuit (QuantumCircuit): Decomposed UCCSD circuit ready for VQE.
    """
    # 1. Generate the reference Hartree-Fock state
    initial_state = HartreeFock(
        num_spatial_orbitals=problem.num_spatial_orbitals,
        num_particles=problem.num_particles,
        qubit_mapper=mapper,
    )

    # 2. Build the UCCSD operator
    ucc = UCCSD(
        num_spatial_orbitals=problem.num_spatial_orbitals,
        num_particles=problem.num_particles,
        qubit_mapper=mapper,
        initial_state=initial_state,
    )
    
    # Decomposing converts the EvolvedOp into a gate-based QuantumCircuit
    circuit = ucc.decompose()
    circuit.name = "UCCSD"
    return circuit


def create_hardware_efficient_ansatz(
    num_qubits: int, 
    reps: int = 3, 
    initial_state_label: str | None = None
) -> QuantumCircuit:
    """
    Hardware-efficient ansatz utilizing primitive_factory helpers for custom initialization.
    
    Inputs:
        num_qubits (int): Number of qubits in the circuit.
        reps (int): Number of entangling layers.
        initial_state_label (str): Label for state prep (e.g., 'plus', 'bell', 'x_++').
    Outputs:
        full_ansatz (QuantumCircuit): The composed hardware-efficient circuit.
    """
    base_ansatz = EfficientSU2(
        num_qubits=num_qubits,
        reps=reps,
        entanglement="linear"
    )

    if initial_state_label is None:
        return base_ansatz

    init_circ = QuantumCircuit(num_qubits)

    if initial_state_label == "plus":
        qr = QuantumRegister(num_qubits)
        init_circ.compose(create_plus_state(qr), inplace=True)

    elif initial_state_label == "bell" and num_qubits >= 2:
        # Assumes entanglement between the first two qubits
        attach_bell_state_prep(init_circ, 0, 1)

    elif initial_state_label.startswith("x_"):
        label = initial_state_label[2:]
        x_prep = get_x_basis_prep_circuit(label)
        init_circ.compose(x_prep, qubits=range(len(label)), inplace=True)

    full_ansatz = init_circ.compose(base_ansatz)
    full_ansatz.name = f"HEAnsatz_{initial_state_label}_reps{reps}"
    return full_ansatz