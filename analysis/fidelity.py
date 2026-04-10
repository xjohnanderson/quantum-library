# analysis/fidelity.py
 
from typing import Union, List
import numpy as np
from qiskit.quantum_info import (
    Statevector,
    DensityMatrix,
    state_fidelity,      
)


def is_pure_state(state: Union[Statevector, DensityMatrix, np.ndarray]) -> bool:
    """Return True if the state is pure (purity = Tr(ρ²) = 1)."""
    if isinstance(state, Statevector):
        return True
    if isinstance(state, np.ndarray):
        state = DensityMatrix(state) if state.ndim == 2 else Statevector(state)
    return np.isclose(state.purity(), 1.0, atol=1e-10)


def compute_fidelity(
    state1: Union[Statevector, DensityMatrix, np.ndarray],
    state2: Union[Statevector, DensityMatrix, np.ndarray],
) -> float:
    """Fidelity F(ρ, σ) between any two states (pure or mixed)."""
    # Auto-convert numpy arrays
    if isinstance(state1, np.ndarray):
        state1 = DensityMatrix(state1) if state1.ndim == 2 else Statevector(state1)
    if isinstance(state2, np.ndarray):
        state2 = DensityMatrix(state2) if state2.ndim == 2 else Statevector(state2)

    return float(state_fidelity(state1, state2))


def compute_trace_distance(
    state1: Union[Statevector, DensityMatrix, np.ndarray],
    state2: Union[Statevector, DensityMatrix, np.ndarray],
) -> float:
    """Trace distance D(ρ, σ) = (1/2)‖ρ − σ‖₁ (pure or mixed).

    Implemented manually so it works on every Qiskit version.
    """
    if isinstance(state1, np.ndarray):
        state1 = DensityMatrix(state1) if state1.ndim == 2 else Statevector(state1)
    if isinstance(state2, np.ndarray):
        state2 = DensityMatrix(state2) if state2.ndim == 2 else Statevector(state2)

    # Convert to DensityMatrix if needed
    if isinstance(state1, Statevector):
        state1 = DensityMatrix(state1)
    if isinstance(state2, Statevector):
        state2 = DensityMatrix(state2)

    # ρ - σ is Hermitian → trace norm = sum of absolute eigenvalues
    diff = state1 - state2
    evals = np.linalg.eigvalsh(diff.data)
    return 0.5 * float(np.sum(np.abs(evals)))


def create_mixed_state(
    pure_states: List[Statevector], probabilities: List[float]
) -> DensityMatrix:
    """Convenience: build a classical mixture Σ p_i |ψ_i⟩⟨ψ_i|."""
    if len(pure_states) != len(probabilities):
        raise ValueError("pure_states and probabilities must have same length")
    if not np.isclose(sum(probabilities), 1.0):
        raise ValueError("probabilities must sum to 1")

    dim = pure_states[0].dim
    rho = np.zeros((dim, dim), dtype=complex)
    for psi, p in zip(pure_states, probabilities):
        rho += p * DensityMatrix(psi).data
    return DensityMatrix(rho)


__all__ = [
    "compute_fidelity",
    "compute_trace_distance",
    "is_pure_state",
    "create_mixed_state",
]