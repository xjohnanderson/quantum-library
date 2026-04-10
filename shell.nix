{ pkgs ? import <nixpkgs> { config.allowBroken = true; } }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
    stdenv.cc.cc.lib
    zlib
    libgcc
  ];

  shellHook = ''
    # This is the magic sauce for pip-installed numpy/qiskit
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib pkgs.zlib pkgs.libgcc ]}:$LD_LIBRARY_PATH"
    
    echo "🚀 Qiskit Hybrid Environment Loaded"
    
    if [ -d ".venv" ]; then
      source .venv/bin/activate
      echo "✅ Virtual environment activated"
    else
      echo "💡 Run 'python -m venv .venv && source .venv/bin/activate && pip install qiskit qiskit-aer' to start."
    fi
  '';
}