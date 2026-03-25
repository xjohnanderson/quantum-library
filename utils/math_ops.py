# utils/math_ops.py
# This script provides classical mathematical utilities for quantum algorithms.

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

def get_period_from_phase(measured_int: int, n_count: int, N: int) -> int:
    # Function Constraints: Uses continued fractions to find the candidate period 'r'.
    # Inputs: measured_int (int), n_count (int), N (int)
    # Outputs: r (int)
    from fractions import Fraction
    phase = measured_int / (2**n_count)
    frac = Fraction(phase).limit_denominator(N)
    return frac.denominator