{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      devShell = pkgs.mkShell {
        name = "bloggen-2.0-dev";
        buildInputs = with pkgs; [
          python311
          python311Packages.numpy
          python311Packages.black
          python311Packages.pytz
          python311Packages.pygithub
          python311Packages.pandas
          python311Packages.matplotlib
          python311Packages.seaborn
          python311Packages.termcolor
          python311Packages.tkinter
        ];
        shellHook = ''
        '';
      };
    });
}
