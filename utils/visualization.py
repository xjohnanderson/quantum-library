# utils/visualization.py
# This module provides flexible visualization for quantum states, operators, and circuits.
# It automatically detects the environment to provide LaTeX, Matplotlib, or ASCII output.

import sys

def _can_render_latex():
    # Function Constraints: Checks if the current environment supports IPython display.
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False

def show_quantum_object(obj, label=""):
    # Function Constraints: Displays a Statevector, Operator, or QuantumCircuit.
    # What it does: Renders LaTeX/MPL in Jupyter, ASCII text in Terminal.
    # Inputs: obj (Statevector/Operator/QuantumCircuit), label (str)
    
    if label:
        print(f"\n--- {label} ---")
        
    if _can_render_latex():
        from IPython.display import display
        # If it's a circuit, we try 'mpl', otherwise 'latex'
        if hasattr(obj, 'draw'):
            try:
                # If it's a circuit, 'mpl' is preferred for diagrams
                if type(obj).__name__ == 'QuantumCircuit':
                    display(obj.draw("mpl"))
                else:
                    display(obj.draw("latex"))
            except Exception:
                # Fallback if mpl/pylatexenc is missing in the venv
                display(obj.draw("text"))
    else:
        # Fallback to ASCII for Firebase Studio terminal
        print(obj.draw("text"))

def show_circuit(qc, label=""):
    # Wrapper specifically for QuantumCircuits
    show_quantum_object(qc, label)

def show_state(state, label=""):
    show_quantum_object(state, label)

def show_operator(op, label=""):
    show_quantum_object(op, label)