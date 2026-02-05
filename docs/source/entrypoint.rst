Entrypoint
============


.. rubric:: COMMAND LINE


.. code-block:: python

   # 1. Activate conda environment
   conda activate viennaptm

   # 2. Use entrypoint to run ViennaPTM
   viennaptm --input tests/data/1vii.pdb \
             --modification "A:50=V3H" \
             --output testoutput.pdb


.. rubric:: CONFIG FILE

.. code-block:: python

    input: ./tests/data/1vii.pdb
    modification:
      - "A:50=V3H"
    output: output.pdb
    logger: console
    debug: false


.. rubric:: PARAMETERS


.. list-table::
   :header-rows: 1
   :widths: 1 1 1 1

   * - Parameter
     - Description
     - Explanation
     - Example

   * - --input
     - Input path or PDB identifier
     - | If the input is a string ending with
       | ``.pdb`` or ``.cif``, it is treated
       | as a local file path and converted
       | to :class:`pathlib.Path`.
       |
       | Otherwise, it is interpreted as a
       | PDB database identifier and must be
       | exactly four characters long.
     - | ./tests/data/1vii.cif
       | ./tests/data/1vii.pdb
   * - --modification
     - List of modifications
     - | A modification is a string (str)
       | which consists of "chain_identifier",
       | "residue_number" and
       | "target abbreviation":
       | "A:50=V3H"
       |
       | A list of modifications is also
       | accepted in form of a list of strings
       | (list[str]):
       | [("A", 50), ("A", 55), ("A", 60)]
     - | "A:50=V3H"
       | [("A", 50), ("A", 55), ("A", 60)]
   * - --output
     - Output path or filename
     - | The output filename has to end with
       | ``.pdb`` or ``.cif`` and converts
       | string paths to :class:`pathlib.Path`.
     - output.pdb
   * - --logger
     - Logging to console or file
     - | When logging is set to ``"console"``,
       | the logging will be printed to the
       | console. Otherwise, a log file is used
       | and the value of :attr:`logger` is
       | interpreted as a file path.
     - console or file
   * - --debug
     - Debug mode
     - | Enables verbose debug logging if ``True``.
     - false or true