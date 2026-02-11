Installation
============

.. rubric:: CREATE CONDA ENVIRONMENT (optional)

.. code-block:: bash

    # create & activate environment
    conda create --name viennaptm python=3.11
    conda activate viennaptm


.. rubric:: LATEST STABLE RELEASE

.. code-block:: bash

    # Install the minimal package
    pip install viennaptm

    # Install additional dependencies for 3D protein rendering
    pip install viennaptm[render]


.. rubric:: INSTALL WITH DEVELOPMENT DEPENDENCIES

.. code-block:: bash

    # Install additional dependencies for running tests
    pip install viennaptm[test]

    # Install additional dependencies for documentation generation
    pip install viennaptm[docs]


.. rubric:: INSTALL FROM SOURCE

.. code-block:: bash

    # Clone the repository
    # SSH alternative: git@github.com:viennaptm/viennaptm.git
    git clone https://github.com/viennaptm/viennaptm.git
    cd viennaptm

    # Install from source
    # Add "-e" to install in editable (developer) mode
    pip install .


.. rubric:: INSTALL GROMACS

.. code-block:: bash

    # Install GROMACS from conda-forge
    conda install conda-forge::gromacs
