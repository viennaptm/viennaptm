Entrypoint
============

Vienna-PTM can be used via an entrypoint from the command line, a configuration
file, or custom scripts.


.. rubric:: COMMAND LINE

.. code-block:: bash

    # 1. Activate the conda environment
    conda activate viennaptm

    # 2. Use the entrypoint (CLI) to run Vienna-PTM
    viennaptm --input tests/data/1vii.pdb \
              --modify "A:50=V3H" \
              --output testoutput.pdb

**Help**

The ``help`` parameter shows the available options in detail.

.. code-block:: bash

    viennaptm --help

Alternatively, you can append --help to any command:

.. code-block:: bash

   viennaptm --input tests/data/1vii.pdb --modify "A:50=V3H" --output testoutput.pdb --help


Help message:

.. code-block:: bash

    Options:
      --config
          [Union, default=None]
          Path to a YAML or JSON configuration file (optional).
      --input
          [Union, default=None]
          Input structure, either CIF or PDB.
      --modify
          [Union, default=None]
          Modifications in the form of "A:50=V3H", which means "chain:residue=target".
      --output
          [Union, default=output.pdb]
          Output structure, either CIF or PDB.
      --gromacs.minimize
          [bool, default=False]
          Energy minimize the modified structure.
      --logger
          [Optional, default=console]
          Set logger to either console (default) or provide a file name.
      --debug
          [Optional, default=False]
          If set to true, enable verbose debugging logging.




.. rubric:: CONFIG FILE

.. code-block:: yaml

    # Example configuration file
    input: ./tests/data/1vii.pdb
    modify:
      - "A:50=V3H"
    output: output.pdb
    logger: console
    debug: false

To run Vienna-PTM using a configuration file:

.. code-block:: bash

    viennaptm --config tests/data/example_config.yaml


.. rubric:: PARAMETERS

.. list-table::
   :header-rows: 1
   :widths: 1 2 3 2

   * - Parameter
     - Description
     - Explanation
     - Example

   * - ``--input``
     - Input path or PDB identifier
     - | If the input is a string ending with
       | ``.pdb`` or ``.cif``, it is treated as
       | a local file path and converted to a
       | :class:`pathlib.Path`.
       |
       | Otherwise, the input is interpreted as
       | a PDB database identifier and must be
       | exactly four characters long.
     - | ``./tests/data/1vii.cif`` or
       | ``1vii``

   * - ``--modify``
     - List of modifications
     - | A modification is specified as a
       | string consisting of a
       | ``chain_identifier``, a
       | ``residue_number``, and a
       | ``target_abbreviation``, for example:
       | ``"A:50=V3H"``.
       |
       | Multiple modifications can be provided
       | as a list of strings.
     - | ``"A:50=V3H"`` or
       | ``"A:50=V3H" "A:55=V3H"``

   * - ``--output``
     - Output path or filename
     - | The output filename must end with
       | ``.pdb`` or ``.cif``. String paths are
       | converted to :class:`pathlib.Path`.
     - ``output.pdb``

   * - ``--logger``
     - Logging destination
     - | If set to ``"console"``, log messages
       | are printed to standard output.
       |
       | Otherwise, the value is interpreted as
       | a file path and logging output is
       | written to a file.
     - ``console`` or ``log.txt``

   * - ``--debug``
     - Debug mode
     - | Enables verbose debug logging when
       | set to ``true``.
     - ``false`` or ``true``


.. rubric:: BASH SCRIPT

Example Bash script:

.. code-block:: bash

    #!/usr/bin/env bash

    # Exit immediately if a command fails
    set -e

    # 1. Initialize conda (required outside an interactive shell)
    # Adjust this path if your conda installation is located elsewhere
    source "$(conda info --base)/etc/profile.d/conda.sh"

    # 2. Activate the conda environment
    conda activate viennaptm

    # 3. Run Vienna-PTM
    viennaptm --input tests/data/1vii.pdb \
              --modify "A:50=V3H" \
              --output testoutput.pdb

Save the script as, for example:

| ``run_viennaptm.sh``

Make it executable:

.. code-block:: bash

    chmod +x run_viennaptm.sh

Run it:

.. code-block:: bash

    ./run_viennaptm.sh


.. rubric:: SLURM SCRIPT

Example SLURM submission script:

.. code-block:: bash

    #!/usr/bin/env bash
    #SBATCH --job-name=viennaptm
    #SBATCH --output=viennaptm_%j.out
    #SBATCH --error=viennaptm_%j.err
    #SBATCH --time=01:00:00
    #SBATCH --cpus-per-task=1
    #SBATCH --mem=4G

    # Fail fast on errors and undefined variables
    set -euo pipefail

    echo "Job started on $(hostname) at $(date)"

    # ---- Conda setup ----
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate viennaptm

    # ---- Run Vienna-PTM ----
    viennaptm --input tests/data/1vii.pdb \
              --modify "A:50=V3H" \
              --output testoutput.pdb

    echo "Job finished at $(date)"


**NOTE:** Alternatively, you can skip the conda initialization and directly provide the full path to the Vienna-PTM entrypoint:

.. code-block:: bash

    /path/to/your/installation/bin/viennaptm \
        --input tests/data/1vii.pdb \
        --modify "A:50=V3H" \
        --output testoutput.pdb

Submit the SLURM script to the cluster using:

.. code-block:: bash

    sbatch run_viennaptm.slurm
