<!-- Logo floated to the right -->
<img src="docs/source/_static/logo.png" alt="Vienna-PTM logo" align="right" width="150"/>

# Vienna-PTM 3.0: Modify proteins with post-translational modifications

[![Coverage Status](https://coveralls.io/repos/github/username/project-name/badge.svg?branch=main)](https://coveralls.io/github/username/project-name?branch=main)  
[![PyPI version](https://badge.fury.io/py/viennaptm.svg)](https://pypi.org/project/viennaptm/)  
[![License](https://img.shields.io/github/license/viennaptm/viennaptm.svg)](LICENSE)  
[![Python Version](https://img.shields.io/badge/python-3.9%2B-green.svg)](https://www.python.org/)

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)  
- [Logo and Trademarks](#logo--trademarks)  
- [Authors / Contributors](#authors--contributors)  

---

## Overview


<img src="assets/ptm_example.png" alt="protein example" align="right" width="140"/>

[Vienna-PTM](https://doi.org/10.1093/nar/gkt416) is a software tool developed in the
group of [Prof. Bojan Žagrović](https://www.maxperutzlabs.ac.at/research/research-groups/zagrovic) 
at the [Max Perutz Labs & University of Vienna](https://www.maxperutzlabs.ac.at/). It enables the automated and 
chemically realistic introduction of PTMs into protein three-dimensional structures provided as PDB files.

Vienna-PTM currently supports 256 different enzymatic and non-enzymatic PTMs and performs
geometrically accurate placement of modifications at user-defined sites 
(see [List of PTMs](https://viennaptm.github.io/viennaptm/list_of_ptms.html) for a complete list).

Optionally, users can perform a subsequent energy minimization using the GROMACS molecular
simulation package. This removes unfavorable steric orientations and makes the structure
amenable to downstream processing.

Vienna-PTM is designed to support structural and computational applications,
such as molecular dynamics simulations and structural analysis. Force-field parameters are
provided for the widely used **GROMOS 45A3, 54A7, and 54A8** force-fields, with direct
compatibility with GROMACS.

For full documentation, tutorials, and API reference, please visit the
[Vienna-PTM Documentation](https://viennaptm.github.io/viennaptm/index.html#).


## Installation

For detailed installation instructions, refer to the [Installation](https://viennaptm.github.io/viennaptm/installation.html) page, and for a step-by-step tutorial, 
consult the [Tutorial](https://viennaptm.github.io/viennaptm/tutorial.html) page in the Documentation.

### Create a new `conda` environment (optional)
```bash
conda create --name viennaptm python=3.11
conda activate viennaptm
```

### Latest stable release
```bash
# Install the minimal package
pip install viennaptm

# Install additional dependencies for 3D protein rendering
pip install viennaptm[render]
```

### Install with development dependencies
```bash
# Install additional dependencies for running tests
pip install viennaptm[test]

# Install additional dependencies for documentation generation
pip install viennaptm[docs]
```

### Install from source
```bash
# Clone the repository
# SSH alternative: git@github.com:viennaptm/viennaptm.git
git clone https://github.com/viennaptm/viennaptm.git
cd viennaptm

# Install from source
# Add "-e" to install in editable (developer) mode
pip install .
```

### Install GROMACS (optional)
`GROMACS` is required only if you wish to perform energy minimization on modified structures.
```bash
conda install conda-forge::gromacs
```

## Usage

### Entrypoint:
For more information, refer to the [Entrypoint](https://viennaptm.github.io/viennaptm/entrypoint.html) page in the documentation.
```bash
# Activate the conda environment
conda activate viennaptm

# Use the entrypoint to run Vienna-PTM
viennaptm --input tests/data/1vii.pdb \
          --modify "A:50=V3H" \
          --output testoutput.pdb
```

### API:
For more information, refer to the [API](https://viennaptm.github.io/viennaptm/api.html) page in the documentation.
```bash
modifier = Modifier()
structure = modifier.modify(
    structure=structure,
    chain_identifier="A",
    residue_number=50,
    target_abbreviation="V3H"
)
```

## Contributing

Contributions from the community are highly welcome. Please consult the
[CONTRIBUTE.md](CONTRIBUTE.md) before submitting changes, in order to help keep the 
code base maintainable, robust, and efficient.


## License

- Code: Apache-2 (see [code licence](https://github.com/viennaptm/viennaptm/blob/development/LICENSE) for more details)
- Resources [including modification libraries]: Attribution-NonCommercial 4.0 International (see [library licence](https://github.com/viennaptm/viennaptm/blob/development/viennaptm/resources/LICENSE) for more details)


## Logo and Trademarks

The project name and logo are the property of the project maintainers. You may use the
logo to refer to or link to this project, but not in a way that suggests endorsement or
affiliation with derivative works without prior permission.


## Authors / Contributors

- **Sophie Margreitter** - [GitHub](https://github.com/SMargreitter)
- **Christian Margreitter** - [GitHub](https://github.com/CMargreitter)  
- **Drazen Petrov** - [GitHub](https://github.com/drazen-petrov)
- **Bojan Žagrović** - [GitHub](https://github.com/bojanzagrovic)


