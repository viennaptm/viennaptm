Installation
============


.. rubric:: LATEST STABLE RELEASE

.. code-block:: python

    # install minimal package
    pip install viennaptm

    # adds dependencies for 3D protein rendering
    pip install viennaptm[render]

    # adds dependencies for test execution
    pip install viennaptm[test]

    # adds dependencies for documenation generation
    pip install viennaptm[docs]


.. rubric:: INSTALL FROM SOURCE

.. code-block:: python

    # clone the repository; SSH alternative: git@github.com:viennaptm/viennaptm.git
    git clone https://github.com/viennaptm/viennaptm.git
    cd viennaptm

    # install from source; add "-e" to install in developer mode
    pip install .


.. rubric:: INSTALL GROMACS

.. code-block:: python

    conda install conda-forge::gromacs


