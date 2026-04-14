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
  '';
}