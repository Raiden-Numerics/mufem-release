# μfem

A finite-element multi-physics application framework based on [mfem](https://mfem.org/), see [μfem](https://raiden-numerics.github.io/mufem-doc/index.html) for more details.

## Validation cases

A collection of validation examples for ([version](VERSION)).

To run the validations please make sure to follow the [Installation instructions](https://raiden-numerics.github.io/mufem-doc/getting_started/installation.html).

To execute a specific case write

```bash
(mufem-env) pymufem Electromagnetics/Compumag-Team1b-Felix-Cylinder/case.py
```

### Electromagnetics

* [**TEAM (Testing Electromagnetic Analysis Methods)**](https://www.compumag.org/wp/team/)

  Introduced in the late 1980s and continuously updated, the TEAM benchmarks focus primarily on low-frequency magnetic problems, providing a standard framework for evaluating numerical methods. Available cases:

  - [Compumag TEAM-1b: The Felix Cylinder](Electromagnetics/Compumag-Team1b-Felix-Cylinder/README.md)
  - [Compumag TEAM 20: 3D Static Force Problem](Electromagnetics/Compumag-Team20-3D-Static-Force-Problem/README.md)
  - [Compumag TEAM 24: Locked Rotor](Electromagnetics/Compumag-Team24-Locked-Rotor/README.md)

## Continuous Integration

[![Run Examples](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/run_cases.yml/badge.svg)](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/run_cases.yml)
[![Python Black](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/black-check.yaml/badge.svg)](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/black-check.yaml)
[![Python flake8](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/flake8.yaml/badge.svg)](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/flake8.yaml)
