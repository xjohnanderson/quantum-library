# analysis/dj_verification.py
# Provides verification for Deutsch-Jozsa circuit results.

def verify_dj_result(counts: dict, n_qubits: int):
    # Function Constraints: Analyzes measurement counts to determine function type.
    # Inputs: counts (dict), n_qubits (int)
    # Outputs: result_summary (dict)
    
    all_zeros_str = '0' * n_qubits
    
    # Calculate probability of the all-zeros state
    total_shots = sum(counts.values())
    zeros_count = counts.get(all_zeros_str, 0)
    prob_zeros = zeros_count / total_shots
    
    # Logical decision
    if prob_zeros > 0.9:  # Threshold for noise/sim robustness
        classification = "CONSTANT"
    else:
        classification = "BALANCED"
        
    return {
        "classification": classification,
        "prob_all_zeros": prob_zeros,
        "raw_counts": counts
    }