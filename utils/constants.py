# utils/constants.py
# This module defines global constants for the qiskit-library.

import numpy as np

# --- Teleportation Register Mapping ---
# [Q, A, B] -> Source, Alice's Ebit, Bob's Ebit
ALICE_SOURCE_INDEX = 0  
ALICE_EBIT_INDEX = 1    
BOB_EBIT_INDEX = 2      

# --- Rotation Constraints ---
THETA_MAX = np.pi
PHI_MAX = 2 * np.pi
LAMBDA_MAX = 2 * np.pi

# --- Naming Conventions ---
QUBIT_NAME = "src_qubit"
ALICE_EBIT_NAME = "alice_ebit"
BOB_EBIT_NAME = "bob_ebit"