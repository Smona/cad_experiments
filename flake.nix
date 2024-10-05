{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
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
          preferWheels = true;
          python = pkgs.python312;
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
              urllib3 = prev.urllib3.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.hatch-vcs ];
              });
              scipy = pkgs.python312Packages.scipy;
              numpy = pkgs.python312Packages.numpy;
              # currently broken in poetry2nix, same error as here:
              # https://github.com/moble/quaternion/issues/155
              numpy-quaternion = pkgs.python312Packages.quaternion;
              casadi = pkgs.python312Packages.casadi;
              voila = prev.voila.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ prev.jupyter-packaging ];
              });
              rtree = pkgs.python312Packages.rtree;
              pyqtwebengine = pkgs.python312Packages.pyqtwebengine;
              pyqt5 = pkgs.python312Packages.pyqt5;
              # https://github.com/nix-community/poetry2nix/issues/1814
              pillow = prev.pillow.overridePythonAttrs (old: {
                # remove pytest-runner
                nativeBuildInputs = [ pkgs.pkg-config ];
              });
              cq-editor = prev.pillow.overridePythonAttrs (old: {
                # remove pytest-runner
                buildInputs = (old.buildInputs or [ ]) ++ [ pkgs.qt5.full ];
              });
              cad-viewer-widget = prev.cad-viewer-widget.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [
                  prev.hatchling
                  prev.hatch-nodejs-version
                  prev.hatch-jupyter-builder
                ];
              });
            }
          );
        }).env.overrideAttrs
          (oldAttrs: {
            buildInputs = [
              pkgs.stdenv.cc
              pkgs.poetry
              pkgs.watchexec
              (pkgs.writeShellScriptBin "start" "watchexec -w test.py python test.py")
              (pkgs.writeShellScriptBin "open" "python open.py && start")
            ];
          });
    };
}
