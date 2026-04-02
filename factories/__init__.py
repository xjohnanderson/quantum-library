# factories/__init__.py
"""Factories package – modular quantum circuit building blocks."""

# Basis (pure Statevectors + constants)
from .basis_factory import (
    get_w_state,
    get_2qubit_z_basis,
    get_2qubit_x_basis,
    get_2qubit_y_basis,
    get_bell_basis,
    get_3qubit_z_basis,
    get_ghz_basis,
    Z_BASIS, X_BASIS, Y_BASIS, BELL_BASIS, GHZ_BASIS,
)

# Primitives
from .primitive_factory import (
    get_swap_gate,
    attach_bell_state_prep,
    attach_bell_measurement,
    get_x_basis_prep_circuit,
    create_zero_state,
    create_plus_state,
    get_composite_operator,
    get_evolution_circuit,
    get_circuit_operator,
)

# Arithmetic gates/circuits — SPLIT INTO TWO CLEAR FACTORIES
from .arithmetic_factory import (
    # Low-level building blocks (used by both factories)
    get_rfa_gate,
    n_bit_adder,

    # MATRIX-BASED FACTORY (fast, compact, RECOMMENDED for Shor demos)
    get_modular_multiplier_gate,
    get_modular_exponentiation_circuit_matrix,

    # ADDER-BASED FACTORY (scalable, RFA + n_bit_adder)
    get_modular_multiplier_circuit,
    get_modular_exponentiation_circuit_adder,
)

# Oracles
from .oracle_factory import (
    get_bit_flip_oracle,
    get_phase_flip_oracle,
    get_bernstein_vazirani_oracle,
    get_dj_oracle,
    create_simon_oracle,
)

# Algorithm-specific components
from .algorithm_factory import (
    get_iqft_circuit,
    get_qft_circuit,
)

# Hamiltonian
from .hamiltonian_factory import (
    get_pauli_op,
    get_hamiltonian_evolution_gate,
)

# State evolution
from .state_factory import (
    get_cz_statevector,
    get_cx_statevector,
    get_cy_statevector,
    get_bv_oracle_statevector,
)

# VQE stuff
from .vqe_factory import (
    create_h2_problem,
    create_uccsd_ansatz,
    create_hardware_efficient_ansatz,
)

__all__ = [name for name in dir() if not name.startswith("_")]