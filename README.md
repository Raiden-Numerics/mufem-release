# mufem-examples

A collection of validation examples for [μfem](http://www.raiden-numerics.com/mufem) ([version](VERSION)).

Install mufem through [pypi](https://pypi.org/project/mufem/) using
```bash
> pip install mufem
```
The run the cases with:
> cd Electromagnetics/Compumag-Team1b-Felix-Cylinder
> pymufem case.py
```
(use `python3 case.py` if you want to run in serial).

## Validation cases

Currently tested with version `v0.1.117`.

### Electromagnetics

- [Compumag TEAM-1b: The Felix Cylinder](Electromagnetics/Compumag-Team1b-Felix-Cylinder/README.md)
- [Compumag TEAM 20: 3D Static Force Problem](Electromagnetics/Compumag-Team20-3D-Static-Force-Problem/README.md)
- [Compumag TEAM 24: Locked Rotor](Electromagnetics/Compumag-Team24-Locked-Rotor/README.md)

## Continuous Integration

[![Run Examples](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/run_cases.yml/badge.svg)](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/run_cases.yml)
[![Python Black](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/black-check.yaml/badge.svg)](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/black-check.yaml)
[![Python flake8](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/flake8.yaml/badge.svg)](https://github.com/Raiden-Numerics/mufem-examples/actions/workflows/flake8.yaml)
