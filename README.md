# Quantum Library

**A clean, modular, educational Qiskit-based quantum computing library.**

Built for rapid prototyping, algorithm verification, and quantum information analysis.  
Perfect for learning, research, and building quantum applications with maximum reusability.

---

## Features

- **Factory Pattern** – Reusable circuit/state building blocks (basis, primitives, oracles, Hamiltonians, VQE ansätze, arithmetic, etc.)
- **Algorithms** – Full implementations of all major quantum algorithms (Deutsch, Bernstein-Vazirani, Grover, QAOA, Shor, Simon, CHSH, Superdense Coding, Teleportation, etc.)
- **Analysis Tools** – State verification, entanglement detection, fidelity, trace distance, concurrence, Helstrom bound
- **Pure & Mixed States Support** – Works seamlessly with `Statevector` and `DensityMatrix`
- **Visualization Ready** – Easy integration with `utils/visualization.py`
- **No-nonsense demos** – Every algorithm and analysis tool has a ready-to-run script
- **Qiskit-native** – Leverages `qiskit.quantum_info` for numerically stable calculations



---

 

### Project Structure

```bash
quantum-library/
├── algorithms/                  # Core quantum algorithms (logic only)
├── analysis/                    # Verification & quantum information tools
│   ├── fidelity.py              # Fidelity + Trace Distance (pure & mixed)
│   ├── entanglement.py          # Purity, entanglement detection, concurrence
│   └── ...
├── factories/                   # Modular building blocks
│   ├── __init__.py
│   ├── basis_factory.py
│   ├── primitive_factory.py
│   ├── oracle_factory.py
│   └── ...
├── scripts/                     # Ready-to-run demos
├── utils/                       # Visualization, math, constants, I/O
├── output/                      # Generated figures
└── README.md
```

### Get Started in Firebase Studio (Cloud IDE)

Firebase Studio has limited system tools, so use this exact sequence:

```bash
nix-shell -p openssh git --run bash
unset PROMPT_COMMAND
python -m venv .venv
source .venv/bin/activate
pip install qiskit qiskit-aer qiskit_algorithms qiskit_nature matplotlib pylatexenc pandas networkx numpy pyscf
```

---
 
 

