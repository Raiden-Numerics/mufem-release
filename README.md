# μfem

A finite-element multi-physics application framework based on [mfem](https://mfem.org/), see [μfem](https://raiden-numerics.github.io/mufem-doc/index.html) for more details.

## Validation cases

A collection of validation examples for ([version](VERSION)).

To run the examples you will need Python version 3.12 installed. We also recommend that you first create a separate Python virtual environment:
```bash
python -m venv ~/mufemEnv
```
Here we assume that the environment data will be stored in the `mufemEnv` folder in your home directory. To activate the newly created Python environment run the following command:
```bash
source ~/mufemEnv/activate
```

Use [pypi](https://pypi.org/project/mufem/) to install the necessary Python libraries:
```bash
pip install numpy matplotlib
```
And, finally, install mufem:
```bash
pip install mufem
```

To launch a specific case, go to the case directory, e.g.
```
cd Electromagnetics/Compumag-Team1b-Felix-Cylinder
```
and execute the case by
```bash
pymufem case.py
```
The command `pymufem` will launch the case in parallel mode. If you want to launch it in serial mode, you can use `python3 case.py` command.

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
