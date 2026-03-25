# utils/visualization.py
# This module provides flexible visualization for quantum states and operators.
# It automatically detects the environment to provide LaTeX or ASCII output.

import sys

def _can_render_latex():
    # Function Constraints: Checks if the current environment supports IPython display.
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            return True
    except ImportError:
        pass
    return False

def show_quantum_object(obj, label=""):
    # Function Constraints: Displays a Statevector or Operator.
    # What it does: Renders LaTeX in Jupyter/IPython, ASCII text in Terminal.
    # Inputs: obj (Statevector/Operator), label (str)
    
    if label:
        print(f"\n--- {label} ---")
        
    if _can_render_latex():
        from IPython.display import display
        display(obj.draw("latex"))
    else:
        # Fallback to ASCII for GitHub Codespaces terminal
        print(obj.draw("text"))

def show_state(state, label=""):
    show_quantum_object(state, label)

def show_operator(op, label=""):
    show_quantum_object(op, label)