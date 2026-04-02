# analysis/resources.py
# This module provides resource estimation for Fault-Tolerant Quantum Computing.

import numpy as np
import pandas as pd
from qiskit import transpile

def print_resource_table(reports):
    # What it does: Renders an FTQC-focused comparison table in the terminal.
    # Inputs: reports (list of dicts containing T-count, Depth, etc.)
    # Outputs: None (Prints to stdout)
    
    header = f"{'Label':<15} | {'L-Qubits':<8} | {'T-Count':<8} | {'CNOTs':<8} | {'Depth':<8}"
    print(header)
    print("-" * len(header))
    
    for r in reports:
        label = r.get("Label", "N/A")
        l_qubits = r.get("Logical Qubits", 0)
        t_count = r.get("T-Count", 0)
        cnots = r.get("CNOT-Count", 0)
        depth = r.get("Depth", 0)
        print(f"{label:<15} | {l_qubits:<8} | {t_count:<8} | {cnots:<8} | {depth:<8}")

def get_resource_report(circuit):
    # Function Constraints: Counts T-gates and Depth in Clifford+T basis.
    t_circ = transpile(circuit, basis_gates=['u', 'cx', 't', 'tdg'], optimization_level=1)
    ops = t_circ.count_ops()
    return {
        "Logical Qubits": circuit.num_qubits,
        "T-Count": ops.get('t', 0) + ops.get('tdg', 0),
        "CNOT-Count": ops.get('cx', 0),
        "Depth": t_circ.depth()
    }

def estimate_physical_overhead(logical_qubits, error_rate=1e-3, target_fidelity=0.99):
    # Function Constraints: Estimates physical qubits using Surface Code scaling.
    # Logic: Physical = 2 * d^2 * Logical_Qubits (approx for Surface Code)
    
    # Simple heuristic for Code Distance (d) based on error rates:
    # d is the number of physical qubits across one dimension of the lattice.
    if error_rate > 1e-4:
        d = 15  # Distance required for high suppression
    else:
        d = 7   # Lower distance for better hardware
        
    physical_per_logical = 2 * (d**2)
    total_physical = logical_qubits * physical_per_logical
    
    return {
        "Code Distance (d)": d,
        "Physical/Logical Ratio": physical_per_logical,
        "Total Physical Qubits": total_physical
    }