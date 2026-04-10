# utils/math_ops.py
# This script provides classical mathematical utilities for quantum algorithms.

import numpy as np
import numpy.typing as npt
from fractions import Fraction

def get_mod_inv(a: int, m: int) -> int:
    # Finds the modular multiplicative inverse using the Extended Euclidean Algorithm.
   
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        return None  # Inverse doesn't exist
    else:
        return x % m

def get_period_from_phase(measured_int: int, n_count: int, N: int, a: int) -> int:
    """Improved continued-fraction post-processing.
    Tries multiple convergents and verifies a^r ≡ 1 (mod N)."""
    if measured_int == 0:
        return 1

    q = 1 << n_count
    frac = Fraction(measured_int, q)

    # Get several good convergents
    convergents = frac.limit_denominator(N).convergents() if hasattr(frac, 'convergents') else [frac.limit_denominator(N)]

    for conv in convergents:
        r = conv.denominator
        if r > N or r == 0:
            continue
        # Verify the period is correct
        if pow(a, r, N) == 1:
            return r

    # Fallback: try small multiples
    for k in range(1, 10):
        r = conv.denominator * k
        if r > N:
            break
        if pow(a, r, N) == 1:
            return r

    return conv.denominator 

def pauli_decomposition(hamiltonian_matrix: npt.NDArray[np.complex128]) -> dict[str, float]:    
    # Decomposes a 2x2 Hermitian matrix into Pauli coefficients.
    # H = cI*I + cX*X + cY*Y + cZ*Z
  
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    
    paulis = [I, X, Y, Z]
    labels = ['I', 'X', 'Y', 'Z']
    coeffs = {}
    
    for i, P in enumerate(paulis):
        # c_j = 1/2 * Tr(P_j * H)
        c_j = 0.5 * np.trace(np.dot(P, hamiltonian_matrix))
        coeffs[labels[i]] = np.real(c_j)
        
    return coeffs