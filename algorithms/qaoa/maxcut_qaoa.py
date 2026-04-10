import numpy as np
import networkx as nx
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
from qiskit.quantum_info import SparsePauliOp

from factories.hamiltonian_factory import get_pauli_op   


def get_maxcut_hamiltonian(graph: nx.Graph) -> SparsePauliOp:
    # MaxCut Ising Hamiltonian using the shared factory 
    num_nodes = graph.number_of_nodes()
    quadratic = {(i, j): 1.0 for i, j in graph.edges()}
    return get_pauli_op(num_nodes, linear={}, quadratic=quadratic)


def run_maxcut_qaoa(graph: nx.Graph, p: int = 1):
    hamiltonian = get_maxcut_hamiltonian(graph)
    optimizer = COBYLA()
    sampler = Sampler()
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=p)
    result = qaoa.compute_minimum_eigenvalue(hamiltonian)
    return result


# Example
if __name__ == "__main__":
    G = nx.cycle_graph(4)
    res = run_maxcut_qaoa(G, p=2)
    print(f"Most likely solution bitstring: {res.best_measurement['bitstring']}")