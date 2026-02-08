Tutorial
============


.. rubric:: HOW TO USE VIENNA PTM

When the installation of ViennaPTM and GROMACS is finished (please see the :doc:`installation` page for all the
necessary steps) you have multiple ways of running it.

The entrypoint allows a quick and easy usage either via command line input (CLI) or configuration file (config file).
The Application Programming Interface (API) offers even more possibilities to adapt ViennaPTM to specific user
requirements and is therefore a favoured option when proprietary data, batch processing or advanced user
modifications are needed.

This user journey starts with an example for a CLI usage.

.. rubric:: COMMAND LINE

**1. Environment**

To run ViennaPTM you first need to activate the conda environment in your console (terminal):

.. code-block:: python

   conda activate viennaptm


.. image:: _static/example.png


**2. Run**

Then use the entrypoint command line to generate the desired posttranslational modifications. For a more detailed
explanation of the available parameters please check the :doc:`entrypoint` page.

.. code-block:: python

   viennaptm --input tests/data/1vii.pdb \
             --modify "A:50=V3H" \
             --output testoutput.pdb


.. image:: _static/parameter_console_input.png


**2. Finish**

Congratulations, you have just generated your first ViennaPTM run and they can now be accessed via the (user given)
output file (here: testoutput.pdb).

.. image:: _static/finished_run.png





.. rubric:: CONFIG FILE

For repetitive runs a config file might be useful as it is less prone to typos or mistakes.

**1. Generate file**

Start by generating a config file in `yaml <https://yaml.org/spec/1.2.2/>`__ format. For the available ViennaPTM parameter check the
:doc:`entrypoint` page.

Config file example:

.. code-block:: python


    input: ./tests/data/1vii.pdb
    modify:
      - "A:50=V3H"
    output: output.pdb
    logger: console
    debug: false


Another config file example:

.. code-block:: python


    input: ./tests/data/1vii.cif
    modify:
      - [("A", 50), ("A", 55), ("A", 60)]
    output: output.pdb
    logger: logger_test_file
    debug: true


**2. Run**

Run the config file via the console.

.. code-block:: python


    viennaptm --config tests/data/example_config.yaml


.. image:: _static/config.png

**3. Selectively override**

You can still selectively override certain parameters. Simply add those changes to the end of
the code line. In the first example config file the ``console`` parameter was set to "console" (--logger console) which
prints directly to the console. If you want to save that information in a file instead, add the logger
parameter with "file" as setting (--logger file) to the end of the config file call:

.. code-block:: python


   viennaptm --config tests/data/example_config.yaml --logger file


.. image:: _static/logger_override.png

You can change all the available ViennaPTM parameters that way. Even multiple changes at once are possible. Here is
an example, how to change the logger as well as the input from a "1vii.pdb" (stated in the first example config
file) to a "1vii.cif":

.. code-block:: python


   viennaptm --config tests/data/example_config.yaml --logger file --input tests/data/1vii.cif
