# scripts/teleportation_demo.py
# Function Constraints: Validates teleportation fidelity using Statevector post-selection.
# This script prepares the state PRIOR to protocol logic to avoid overwriting entanglement.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import random
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.circuit.library import UGate

from utils.constants import ALICE_SOURCE_INDEX, THETA_MAX, PHI_MAX, LAMBDA_MAX
from algorithms.teleportation.logic import get_teleportation_circuit
from analysis.fidelity import check_transfer_integrity
from utils.visualization import show_state

def run_teleportation_demo():
    print("=== QUANTUM TELEPORTATION: NUMERICAL PROOF ===")
    
    # 1. Prepare a Random Target State (The "Message")
    theta = random.random() * THETA_MAX
    phi = random.random() * PHI_MAX
    lam = random.random() * LAMBDA_MAX
    target_gate = UGate(theta, phi, lam)
    
    target_sv = Statevector.from_instruction(target_gate)
    target_rho = DensityMatrix(target_sv)
    
    # 2. Sequential Circuit Construction
    # Initialize 3-qubit register
    qr = QuantumRegister(3, name="q")
    qc = QuantumCircuit(qr)
    
    # FIRST: Prepare the message state on Alice's source qubit
    # This must happen first so prepare_state doesn't reset existing gates.
    qc.prepare_state(target_sv, [ALICE_SOURCE_INDEX])
    qc.barrier()
    
    # SECOND: Append the teleportation infrastructure (Simulation Mode)
    # This builds the Bell pair and performs Alice's basis change.
    tele_logic = get_teleportation_circuit(simulation_mode=True)
    qc.compose(tele_logic, inplace=True)
    
    # 3. Mathematical Extraction (Simulating the '00' branch)
    sv = Statevector.from_instruction(qc)
    
    # Qiskit indexing for 3 qubits: |q2 (Bob) q1 (Alice-ebit) q0 (Alice-Source)>
    # Indices 0 (|000>) and 4 (|100>) represent the state of Bob's qubit
    # when the partial measurement of q1 and q0 yields '00'.
    c0 = sv.data[0]
    c4 = sv.data[4]
    
    branch_coeffs = np.array([c0, c4])
    
    # Re-normalize the extracted branch amplitudes
    norm = np.linalg.norm(branch_coeffs)
    if norm == 0:
        print("[ERROR] Branch probability is zero. Verify circuit connectivity.")
        return

    bob_vec = branch_coeffs / norm
    bob_rho = DensityMatrix(np.outer(bob_vec, bob_vec.conj()))
    
    # 4. Verification via Analysis Module
    fidelity, is_match = check_transfer_integrity(target_rho, bob_rho)
    
    # 5. Output Results
    print(f"Input Rotation: θ={theta:.4f}, φ={phi:.4f}")
    print("-" * 40)
    show_state(target_rho, "Alice's Input (Target)")
    show_state(bob_rho, "Bob's Reconstructed State")
    print("-" * 40)
    print(f"STATE FIDELITY: {fidelity * 100:.6f}%")
    
    if is_match:
        print("[VERDICT] SUCCESS: Teleportation verified via identical Density Matrices.")
    else:
        print("[VERDICT] FAILURE: State divergence detected.")

if __name__ == "__main__":
    run_teleportation_demo()