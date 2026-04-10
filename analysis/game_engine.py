# analysis/game_engine.py
# This module provides a generalized execution engine for binary-input/binary-output games.
# It is designed to benchmark classical vs. quantum strategies.

import random

def run_binary_game(strategy_func, num_trials=1000, game_type="CHSH"):
    # Function Constraints: Executes a game loop and calculates the win rate.
    # What it does: Generates random inputs, queries a strategy, and validates the win condition.
    # Inputs: strategy_func (callable), num_trials (int), game_type (str)
    # Outputs: win_rate (float)
    
    wins = 0
    
    for _ in range(num_trials):
        # 1. Generate random binary inputs for Alice (x) and Bob (y)
        x, y = random.randint(0, 1), random.randint(0, 1)
        
        # 2. Get outputs from the provided strategy (Classical or Quantum)
        a, b = strategy_func(x, y)
        
        # 3. Validate Win Condition based on game_type
        if game_type == "CHSH":
            # CHSH Condition: a XOR b == x AND y
            if (int(a) ^ int(b)) == (x & y):
                wins += 1
        else:
            raise ValueError(f"Unsupported game_type: {game_type}")
            
    return wins / num_trials

def report_game_stats(win_rate, strategy_label):
    # Function Constraints: Prints a formatted summary of game performance.
    # Inputs: win_rate (float), strategy_label (str)
    
    print(f"--- {strategy_label} Performance ---")
    print(f"Win Rate: {win_rate:.2%}")
    
    # Contextual verification based on the CHSH Bell Limit (75%)
    if win_rate > 0.76:
        print("Result: Quantum Advantage Confirmed (Bell Violation).")
    elif win_rate > 0.70:
        print("Result: Classical Limit Observed (~75%).")
    print("-" * 35)