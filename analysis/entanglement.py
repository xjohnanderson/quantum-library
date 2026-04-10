# analysis/entanglement.py

from typing import Tuple, Union
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

 
from .fidelity import compute_trace_distance, is_pure_state


def state_purity(state: Union[Statevector, DensityMatrix, np.ndarray]) -> float:
    """Return Tr(ρ²) as a clean real float  """
    if isinstance(state, Statevector):
        return 1.0
    if isinstance(state, np.ndarray):
        state = DensityMatrix(state) if state.ndim == 2 else Statevector(state)
    # purity() can return complex due to tiny numerical imag part
    return float(np.real(state.purity()))


def verify_entanglement(
    state: Union[Statevector, DensityMatrix, np.ndarray],
    subsystem_to_trace: list[int] = [1]
) -> Tuple[bool, float]:
    """
    Checks if a bipartite (or multi-partite) state is entangled.

    Strategy: purity of any reduced subsystem < 1 ⇒ entangled.
    Works for both pure and mixed global states.
    """
    if isinstance(state, Statevector) or (isinstance(state, np.ndarray) and state.ndim == 1):
        rho = DensityMatrix(state)
    else:
        rho = DensityMatrix(state) if isinstance(state, np.ndarray) else state

    rho_reduced = partial_trace(rho, subsystem_to_trace)
    purity = state_purity(rho_reduced)

    threshold = 0.999 if is_pure_state(rho) else 0.99
    is_entangled = purity < threshold

    return is_entangled, purity


def helstrom_bound(
    state1: Union[Statevector, DensityMatrix, np.ndarray],
    state2: Union[Statevector, DensityMatrix, np.ndarray],
    prior: float = 0.5
) -> Tuple[float, float]:
    """
    Helstrom bound for optimal discrimination between two states.
    Returns (success_probability, error_probability).
    """
    D = compute_trace_distance(state1, state2)

    if abs(prior - 0.5) < 1e-10:
        success = (1 + D) / 2
        error = (1 - D) / 2
    else:
        success = prior * (1 + D) + (1 - prior) * (1 - D)
        error = 1 - success

    return float(success), float(error)


def compute_concurrence(
    state: Union[Statevector, DensityMatrix, np.ndarray]
) -> float:
    """
    Concurrence C(ρ) for a 2-qubit state (pure or mixed).

    Formula:
        C(ρ) = max(0, λ₁ − λ₂ − λ₃ − λ₄)
    where λi are the square roots of the eigenvalues (in decreasing order)
    of the matrix R = ρ (σ_y ⊗ σ_y) ρ* (σ_y ⊗ σ_y).

    Returns a real number ∈ [0, 1]:
        C = 1 → maximally entangled (e.g. Bell states)
        C = 0 → separable
    """
    # Convert to DensityMatrix (2-qubit only)
    if isinstance(state, Statevector) or (isinstance(state, np.ndarray) and state.ndim == 1):
        rho = DensityMatrix(state)
    else:
        rho = DensityMatrix(state) if isinstance(state, np.ndarray) else state

    if rho.dim != 4:
        raise ValueError("compute_concurrence is only defined for 2-qubit states (dim=4)")

    # Pauli Y
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    YY = np.kron(sigma_y, sigma_y)

    # Spin-flipped state: ρ̃ = (σy⊗σy) ρ* (σy⊗σy)
    rho_tilde = YY @ rho.conjugate().data @ YY

    # R = ρ ρ̃
    R = rho.data @ rho_tilde

    # Eigenvalues of R, take sqrt of absolute values, sort descending
    evals = np.sqrt(np.abs(np.linalg.eigvals(R)))
    evals = np.sort(evals)[::-1]

    # Concurrence
    C = max(0.0, evals[0] - evals[1] - evals[2] - evals[3])
    return float(C)


def is_entangled(state: Union[Statevector, DensityMatrix, np.ndarray]) -> bool:
    """Convenience wrapper that returns only the boolean."""
    entangled, _ = verify_entanglement(state)
    return entangled


__all__ = [
    "state_purity",
    "verify_entanglement",
    "helstrom_bound",
    "compute_concurrence",
    "is_entangled",
]