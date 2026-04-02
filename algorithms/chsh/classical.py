# algorithms/chsh/classical.py
# This script implements the optimal deterministic classical strategy for CHSH.
# Theory: No local hidden variable theory can exceed a 75% win rate.

def classical_strategy(x: int, y: int):
    # Function Constraints: Implements the "Always Zero" strategy.
    # What it does: Alice and Bob ignore their inputs (x, y) and output 0.
    # Inputs: x (int), y (int)
    # Outputs: tuple (a, b) as strings
    
    # In the optimal classical strategy, Alice and Bob agree to 
    # output a=0 and b=0. 
    # This wins when (0 ^ 0) == (x & y), which is true for:
    # (0,0), (0,1), and (1,0). It only fails for (1,1).
    
    a = 0
    b = 0
    
    return str(a), str(b)