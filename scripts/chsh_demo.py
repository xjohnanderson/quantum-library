# scripts/chsh_demo.py
# Demo: Proving Bell's Inequality violation via the CHSH Game.

import sys
import os
import random

# Append project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we can import from the root packages
from algorithms.chsh.logic import quantum_strategy
# Assuming classical_strategy is defined in your algorithms directory
from algorithms.chsh.classical import classical_strategy  

def run_chsh_experiment(strategy_func, num_games=1000):
    # Win condition: (a ⊕ b) == (x ∧ y)
    wins = 0
    for _ in range(num_games):
        # Generate random inputs x, y ∈ {0, 1}
        x, y = random.randint(0, 1), random.randint(0, 1)
        
        # Get bits a, b from the strategy
        a, b = strategy_func(x, y)
        
        # Check XOR of outputs vs AND of inputs
        if (int(a) ^ int(b)) == (x & y):
            wins += 1
    return wins / num_games

if __name__ == "__main__":
    N = 1000
    print("--- CHSH Non-Locality Experiment ---")
    
    q_score = run_chsh_experiment(quantum_strategy, N)
    c_score = run_chsh_experiment(classical_strategy, N)
    
    print(f"Classical Win Rate: {c_score:.2%} (Limit: 75%)")
    print(f"Quantum Win Rate:   {q_score:.2%} (Limit: 85%)")
    
    if q_score > 0.75:
        print("\n[VERDICT] Bell's Inequality Violated: Quantum correlations detected.")