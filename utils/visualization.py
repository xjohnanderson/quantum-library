# utils/visualization.py
# Path: utils/visualization.py

import os
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector

def _can_render_latex():
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False

def show_quantum_object(obj, label="", save_path=None):
    if label:
        print(f"\n--- {label} ---")
        
    if type(obj).__name__ == 'QuantumCircuit' and save_path:
        obj.draw("mpl").savefig(save_path)
        print(f"[Visualized] Circuit saved to: {save_path}")

    if _can_render_latex():
        from IPython.display import display
        try:
            display(obj.draw("mpl") if type(obj).__name__ == 'QuantumCircuit' else obj.draw("latex"))
        except:
            display(obj.draw("text"))
    else:
        print(obj.draw("text") if hasattr(obj, 'draw') else str(obj))

def show_bloch_comparison(states, labels=None, save_path=None):
    """
    Renders Bloch Spheres for state comparison.
    Tensors individual 1-qubit states into a multi-qubit object for side-by-side plotting.
    """
    # Tensor target_rho ^ bob_rho to create a 2-qubit system (4x4 matrix)
    combined_state = states[0]
    for i in range(1, len(states)):
        combined_state = combined_state.tensor(states[i])

    fig = plot_bloch_multivector(combined_state, title="State Comparison")
    
    # Optional annotation for Alice/Bob
    if labels and len(labels) >= 2:
        fig.text(0.25, 0.1, labels[1], ha='center', fontsize=10) # Bob (Left)
        fig.text(0.75, 0.1, labels[0], ha='center', fontsize=10) # Alice (Right)

    if _can_render_latex():
        from IPython.display import display
        display(fig)
    
    if save_path:
        fig.savefig(save_path)
        plt.close(fig)
        print(f"[Visualized] Bloch Plot saved to: {save_path}")
    elif not _can_render_latex():
        print("\n[INFO] Bloch Sphere skipped (Terminal Mode & No save_path).")

def show_circuit(qc, label="", save_path=None):
    show_quantum_object(qc, label, save_path=save_path)

def show_state(state, label=""):
    show_quantum_object(state, label)