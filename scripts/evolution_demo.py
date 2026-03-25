# scripts/evolution_demo.py
# Function Constraints: Verifies Unitary transformation H-T-H-S-Y.
# Logic: Final state should match the first column of the circuit's Unitary operator.

import sys
import os

# Append project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from factories import Z_BASIS, get_evolution_circuit, get_circuit_operator
from utils.visualization import show_state, show_operator

def run_evolution_demo():
    # 1. Initialize State (|00>)
    initial_ket = Z_BASIS['00'] 
    
    # 2. Setup the H-T-H-S-Y Circuit
    circuit = get_evolution_circuit()
    
    # 3. Operations: Evolve the statevector
    # The evolve method applies the circuit's unitary to the Statevector.
    final_state = initial_ket.evolve(circuit)
    circuit_op = get_circuit_operator(circuit)
    
    # 4. Outputs: Use your new visualization hub
    show_state(final_state, label="Final State Vector (|ψ⟩)")
    show_operator(circuit_op, label="Unitary Evolution Matrix (U)")
    
    print("\nSimulation Complete. State evolved through H-T-H-S-Y sequence.")

if __name__ == "__main__":
    run_evolution_demo()