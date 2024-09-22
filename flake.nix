{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-24.05";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs =
    {
      self,
      nixpkgs,
      poetry2nix,
    }:
    {
      devShell.x86_64-linux =
        let
          pkgs = nixpkgs.legacyPackages.x86_64-linux;
          p2n = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
        in
        (p2n.mkPoetryEnv {
          projectDir = ./.;
          overrides = p2n.defaultPoetryOverrides.extend (
            final: prev: {
              trianglesolver = prev.trianglesolver.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
              });
              svgpathtools = prev.svgpathtools.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
              });
              ocpsvg = prev.ocpsvg.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
              });
              yacv-server = prev.yacv-server.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.poetry ];
              });
            }
          );
        }).env.overrideAttrs
          (oldAttrs: {
            buildInputs = [
              pkgs.poetry
              pkgs.watchexec
              (pkgs.writeShellScriptBin "start" "watchexec -w test.py python test.py")
              (pkgs.writeShellScriptBin "open" "python open.py && start")
            ];
          });
    };
}
