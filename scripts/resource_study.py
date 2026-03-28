# scripts/resource_study.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from factories import get_rfa_gate
from algorithms.arithmetic.adder import n_bit_adder
from analysis.resources import get_resource_report, estimate_physical_overhead

def run_future_forecast():
    n = 4
    adder = n_bit_adder(n)
    res = get_resource_report(adder)
    
    # Forecast for "Near-Term" vs "Ideal" hardware
    near_term = estimate_physical_overhead(res["Logical Qubits"], error_rate=1e-3)
    
    print(f"--- Forecast for {n}-bit Adder ---")
    print(f"Logical Qubits required: {res['Logical Qubits']}")
    print(f"T-Gate Bottleneck:      {res['T-Count']}")
    print(f"Physical Qubits needed (Surface Code): {near_term['Total Physical Qubits']}")

if __name__ == "__main__":
    run_future_forecast()