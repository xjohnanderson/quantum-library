# scripts/kickback_demo.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from factories import X_BASIS, get_bit_flip_oracle
from analysis.kickback import verify_kickback



def run_kickback_analysis(case_label, control_sign, target_sign):
    # Function Constraints: Verifies phase kickback for a specific oracle case.
    label = f"{control_sign}{target_sign}"
    pre_oracle_state = X_BASIS[label]
    
    oracle_gate = get_bit_flip_oracle(case_label)
    post_oracle_state = pre_oracle_state.evolve(oracle_gate)
    
    detected, _ = verify_kickback(pre_oracle_state, post_oracle_state)
    
    print(f"--- Oracle: {case_label} | Input: |{label}> ---")
    print(f"Kickback Detected: {detected}")
    if detected:
        # Show the actual statevector shift
        print(f"State Shift:\n{post_oracle_state.draw('text')}")

if __name__ == "__main__":
    print("ANALYZING PHASE KICKBACK PHENOMENA\n" + "="*40)
    # Proof: Balanced oracles trigger kickback with |-> targets
    run_kickback_analysis('b0', '+', '-') 
    
    # Proof: Constant oracles do not trigger relative phase kickback
    run_kickback_analysis('c1', '+', '-')