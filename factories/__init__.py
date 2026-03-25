# factories/__init__.py
#Factories package
#Provides modular components for quantum circuits, state preparation,
#and common quantum information objects.
 

# Basis factory exports
from .basis_factory import (
    get_w_state,
    get_2qubit_z_basis,
    get_2qubit_x_basis,
    get_2qubit_y_basis,
    get_bell_basis,
    get_3qubit_z_basis,
    get_ghz_basis,
    # Constants
    Z_BASIS,
    X_BASIS,
    Y_BASIS,
    BELL_BASIS,
    GHZ_BASIS,
)

# Circuit factory exports
from .circuit_factory import (
    # Bell helpers
    attach_bell_state_prep,
    attach_bell_measurement,
    
    # CHSH
    get_chsh_circuit,
    
    # Grover
    get_diffuser,
    
    # Oracles
    get_bit_flip_oracle,
    get_phase_flip_oracle,
    
    # Custom gates
    get_rfa_gate,
    
    # State preparation
    get_x_basis_prep_circuit,
    
    # Fourier transforms
    get_iqft_circuit,
    get_qft_circuit,
    
    # Operator utilities
    get_composite_operator,
    get_evolution_circuit,
    get_circuit_operator,
)

# State factory exports
from .state_factory import (
    get_cz_statevector,
    get_cx_statevector,
    get_cy_statevector,
)

# Optional: Create convenient grouped imports
__all__ = [
    # Basis
    "get_w_state",
    "get_2qubit_z_basis",
    "get_2qubit_x_basis",
    "get_2qubit_y_basis",
    "get_bell_basis",
    "get_3qubit_z_basis",
    "get_ghz_basis",
    "Z_BASIS",
    "X_BASIS",
    "Y_BASIS",
    "BELL_BASIS",
    "GHZ_BASIS",
    
    # Circuit components
    "attach_bell_state_prep",
    "attach_bell_measurement",
    "get_chsh_circuit",
    "get_diffuser",
    "get_bit_flip_oracle",
    "get_phase_flip_oracle",
    "get_rfa_gate",
    "get_x_basis_prep_circuit",
    "get_iqft_circuit",
    "get_qft_circuit",
    "get_composite_operator",
    "get_evolution_circuit",
    "get_circuit_operator",
    
    # State evolution
    "get_cz_statevector",
    "get_cx_statevector",
    "get_cy_statevector",
]