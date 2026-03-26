# scripts/arithmetic_demo.py
# Function Constraints: Compares quantum resource scaling for N-bit adders.
# Logic: Analyzes gate depth and qubit count as bit-width increases.

import sys
import os

# Append project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.arithmetic.adder import n_bit_adder
from analysis.resources import get_resource_report, print_resource_table
from utils.visualization import show_circuit  # <--- New Import

def run_scalability_study():
    reports = []
    # Analyzing scaling for 2, 4, and 8-bit quantum addition
    for n in [2, 4, 8]:
        circuit = n_bit_adder(n)
        
        # 1. Visualization (Optional: only show for smaller n to keep terminal clean)
        if n <= 4:
            show_circuit(circuit, label=f"Circuit Architecture: {n}-bit Adder")
        
        # 2. Resource Analysis
        report = get_resource_report(circuit)
        report["Label"] = f"{n}-bit Adder"
        reports.append(report)
    
    print("\n" + "="*50)
    print("--- QUANTUM ARITHMETIC SCALABILITY REPORT ---")
    print("="*50)
    print_resource_table(reports)

if __name__ == "__main__":
    run_scalability_study()