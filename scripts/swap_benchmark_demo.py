# scripts/swap_benchmark_demo.py
import sys 
import os
from qiskit import QuantumCircuit, transpile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from factories import get_swap_gate
from analysis.resources import get_resource_report, print_resource_table
from analysis.fidelity import check_transfer_integrity
from qiskit.quantum_info import Operator

def run_swap_benchmark():
    """
    Compares native Qiskit swap vs. manual 3-CNOT decomposition.
    Normalizes both to Clifford+T basis for resource analysis.
    """
    
    # 1. Manual Decomposition (from primitive_factory)
    qc_manual = QuantumCircuit(2, name="Manual_3_CNOT")
    get_swap_gate(qc_manual, 0, 1)
    
    # 2. Native Qiskit Swap
    qc_native = QuantumCircuit(2, name="Native_Swap")
    qc_native.swap(0, 1)
    
    # 3. Functional Verification (Fidelity)
    # Convert both to Operators to ensure they represent the same unitary
    op_manual = Operator(qc_manual)
    op_native = Operator(qc_native)
    
    
    # Note: Using state_fidelity logic requires density matrices or ops
    is_equivalent = np.allclose(op_manual.data, op_native.data)
    
    # 4. Resource Estimation
    # get_resource_report transpiles to ['u', 'cx', 't', 'tdg']
    report_manual = get_resource_report(qc_manual)
    report_manual["Label"] = "Manual (3-CX)"
    
    report_native = get_resource_report(qc_native)
    report_native["Label"] = "Native Qiskit"
    
    # 5. Output Results
    print(f"--- Functional Integrity: {'PASSED' if is_equivalent else 'FAILED'} ---\n")
    print_resource_table([report_manual, report_native])

if __name__ == "__main__":
    import numpy as np
    run_swap_benchmark()