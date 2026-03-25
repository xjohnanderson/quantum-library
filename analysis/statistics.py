# analysis/statistics.py
# This module provides statistical post-processing for quantum experiments.

def get_chsh_witness(correlations):
    # Function Constraints: Calculates the S-parameter from a correlation map.
    # Theory: S = |E(0,0) + E(0,1) + E(1,0) - E(1,1)|
    # Inputs: correlations (dict { 'xy': float })
    # Outputs: s_param (float), violated (bool)
    
    e00 = correlations.get('00', 0)
    e01 = correlations.get('01', 0)
    e10 = correlations.get('10', 0)
    e11 = correlations.get('11', 0)
    
    s_param = abs(e00 + e01 + e10 - e11)
    return s_param, s_param > 2.0