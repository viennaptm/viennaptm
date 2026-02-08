# Vienna-PTM 3.0: Modify proteins with post-translational modifications

[![Coverage Status](https://coveralls.io/repos/github/username/project-name/badge.svg?branch=main)](https://coveralls.io/github/username/project-name?branch=main)  
[![PyPI version](https://badge.fury.io/py/viennaptm.svg)](https://pypi.org/project/viennaptm/)  
[![License](https://img.shields.io/github/license/viennaptm/viennaptm.svg)](LICENSE)  
[![Python Version](https://img.shields.io/badge/python-3.9%2B-green.svg)](https://www.python.org/)

---

![Project Logo](_static/viennaptm_logo_c.png)

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)  
- [Authors / Contributors](#authors--contributors)  

---


## Overview
The web server Vienna-PTM is a platform for automated introduction of PTMs of choice to 
protein 3D structures (PDB files) in a user-friendly visual environment. With 256 different 
enzymatic and non-enzymatic PTMs available, the server performs geometrically realistic 
introduction of modifications at sites of interests, as well as subsequent energy minimization. 
Finally, the server makes available force field parameters and input files needed to run 
MD simulations of modified proteins within the framework of the widely used GROMOS 54A7 and 
45A3 force fields and GROMACS simulation package.

![protein_example](_static/ptm_example.png)

## Installation

### Create a new `conda` environment (optional)
```bash
conda create --name viennaptm python=3.11
conda activate viennaptm
```

### Latest stable release
```bash
# install minimal package
pip install viennaptm

# adds dependencies for 3D protein rendering
pip install viennaptm[render]

# adds dependencies for test execution
pip install viennaptm[test]

# adds dependencies for documenation generation
pip install viennaptm[docs]
```

### Install from source
```bash
# clone the repository; SSH alternative: git@github.com:viennaptm/viennaptm.git
git clone https://github.com/viennaptm/viennaptm.git
cd viennaptm

# install from source; add "-e" to install in developer mode
pip install .
```

### Install GROMACS (optional)
`GROMACS` is required for energy minimzation of modified structures.
```bash
conda install conda-forge::gromacs
```

## Usage
### Entrypoint:
```bash
# 1. Activate conda environment
conda activate viennaptm

# 2. Use entrypoint to run ViennaPTM
viennaptm --input tests/data/1vii.pdb \
          --modify "A:50=V3H" \
          --output testoutput.pdb
```

### API:
```bash
modifier = Modifier()
structure = modifier.modify(structure=structure,
                            chain_identifier='A',
                            residue_number=50,
                            target_abbreviation="V3H")
```

## Contributing / Issue reporting
Contributions and issue reports are always welcome, please follow the instructions in the [CONTRIBUTE.md](CONTRIBUTE.md) file.

## License

- Code: Apache-2
- Resources [including modification libraries]: Attribution-NonCommercial 4.0 International


## Authors / Contributors

- **Sophie Margreitter** - [GitHub](https://github.com/SMargreitter)
- **Christian Margreitter** - [GitHub](https://github.com/CMargreitter)  
- **Drazen Petrov** - [GitHub](https://github.com/drazen-petrov)
- **Bojan Zagrovic** - [GitHub](https://github.com/bojanzagrovic)
