# Contribute

Vienna-PTM is constantly evolving, and we are grateful for any contributions - bug fixes, features, issue reports and documentation.
This document outlines best practices, and we kindly ask you to follow them to make the process seamless for everyone!

---

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Check pypi compatibility](#check-pypi-compatibility)
- [Make new release](#make-new-release)


---

## Ways to Contribute

You can contribute by:

- Fixing bugs
- Adding features or enhancements
- Improving documentation (including user journeys and tutorials)
- Writing or improving tests, extending test coverage
- Reviewing pull requests
- Reporting issues or proposing ideas

Not sure where to start? Check the issue tracker for items that are a good foundation to get up to speed.

---

## Getting Started

### Set up the environment
1. Create a local environment and activate it
   ```bash
   conda create --name viennaptm python=3.11
   conda activate viennaptm
2. Install your local version (in development mode) and also install `GROMACS`:
   ```bash
   pip install -e .[test,docs]
   conda install conda-forge::gromacs

### Install development version from source
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/viennaptm.git
   cd viennaptm
   git checkout development
3. Branch off the `development` branch:
   ```bash
   git checkout -b feature/<new-feature-name>
4. Enable `hooks` to ensure all unit tests are executed successfully before every push:
   ```bash
   git config core.hooksPath .githooks
5. Implement your additions / changes
6. Add unit tests as appropriate
7. Add documentation as appropriate
8. Create a Pull Request (PR) as described in these [instructions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)

Make sure that your PR has a clear description. If you hit any problems, e.g. with unit test writing or adding elements to the documentation, create the PR and indicate that more work is needed and help is welcome.

---

## Check pypi compatibility
```shell
pip install .[build]
python -m build
python -m twine check dist/*
```

---

## Make new release
```shell
# ensure 'master' is on correct commit
# execute locally (version to be given in vX.Y.Z format)
git tag v<VERSION>
git push origin v<VERSION>
```
