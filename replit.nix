{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.pytest
    pkgs.python311Packages.pyyaml
    pkgs.python311Packages.jsonschema
  ];
}
