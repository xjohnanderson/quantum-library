{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.gcc
    pkgs.python3
    pkgs.git
    pkgs.openssh
    # Add Node.js here to provide the engine for the Gemini agent
    pkgs.nodejs_20
  ];

  shellHook = ''
    # Existing library paths
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ]}"
    export PYTHONPATH="$PYTHONPATH:$(pwd)"

    # Alias to run the Gemini agent without needing it in the Nix registry
    # The -y flag skips the 'Install package?' prompt
    alias gemini="npx -y @google/gemini-cli@latest"

    echo "-------------------------------------------------------"
    echo "Environment Ready: gcc, python3, git, ssh, and nodejs"
    echo "Type 'gemini' to launch the Gemini Agent"
    echo "-------------------------------------------------------"
  '';
}