# scripts/teleportation_demo.py
import sys
import os
import numpy as np
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.circuit.library import UGate

from utils.constants import ALICE_SOURCE_INDEX, THETA_MAX, PHI_MAX, LAMBDA_MAX
from algorithms.teleportation.logic import get_teleportation_circuit
from analysis.fidelity import check_transfer_integrity
from utils.visualization import show_state, show_circuit, show_bloch_comparison
from utils.io import prepare_output_dir

def run_teleportation_demo():
    print("=== QUANTUM TELEPORTATION: NUMERICAL & GEOMETRIC PROOF ===")
    
    # 0. Initialize Volatile Workspace & Get Script Prefix
    out_dir, prefix = prepare_output_dir()
    
    # 1. Prepare a Random Target State (The "Message")
    theta = random.random() * THETA_MAX
    phi = random.random() * PHI_MAX
    lam = random.random() * LAMBDA_MAX
    target_gate = UGate(theta, phi, lam)
    
    target_sv = Statevector.from_instruction(target_gate)
    target_rho = DensityMatrix(target_sv)
    
    # 2. Sequential Circuit Construction
    qr = QuantumRegister(3, name="q")
    qc = QuantumCircuit(qr)
    qc.prepare_state(target_sv, [ALICE_SOURCE_INDEX])
    qc.barrier()
    
    tele_logic = get_teleportation_circuit(simulation_mode=True)
    qc.compose(tele_logic, inplace=True)
    
    # 3. Mathematical Extraction (Simulating the '00' branch)
    sv = Statevector.from_instruction(qc)
    c0, c4 = sv.data[0], sv.data[4]
    
    branch_coeffs = np.array([c0, c4])
    norm = np.linalg.norm(branch_coeffs)
    
    if norm == 0:
        print("[ERROR] Branch probability is zero. Verify circuit connectivity.")
        return

    bob_vec = branch_coeffs / norm
    bob_rho = DensityMatrix(np.outer(bob_vec, bob_vec.conj()))
    
    # 4. Verification via Analysis Module
    fidelity, is_match = check_transfer_integrity(target_rho, bob_rho)
    
    # 5. Output Results & Visualization
    print(f"Input Rotation: θ={theta:.4f}, φ={phi:.4f}")
    print("-" * 40)
    
    # Define artifact paths using the dynamic prefix
    c_path = os.path.join(out_dir, f"{prefix}_circuit.png")
    b_path = os.path.join(out_dir, f"{prefix}_bloch_comparison.png")
    
    # Visualizing the Protocol Infrastructure
    show_circuit(qc, "Teleportation Infrastructure", save_path=c_path)
    
    # Visualizing the Math
    show_state(target_rho, "Alice's Input State (Density Matrix)")
    show_state(bob_rho, "Bob's Reconstructed State (Density Matrix)")
    
    # Visualizing the Geometry (Bloch Comparison)
    show_bloch_comparison(
        [target_rho, bob_rho], 
        labels=["Alice's Input", "Bob's Output"],
        save_path=b_path
    )
    
    print("-" * 40)
    print(f"STATE FIDELITY: {fidelity * 100:.6f}%")
    
    if is_match:
        print("[VERDICT] SUCCESS: Teleportation verified via identical Density Matrices.")
    else:
        print("[VERDICT] FAILURE: State divergence detected.")

if __name__ == "__main__":
    run_teleportation_demo()