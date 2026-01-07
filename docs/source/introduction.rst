Introduction
============

The web server `Vienna-PTM <https://vienna-ptm.univie.ac.at/>`__ is a platform for automated introduction of PTMs of choice to protein 3D structures (PDB files) in a user-friendly visual environment. With 256 different enzymatic and non-enzymatic PTMs available, the server performs geometrically realistic introduction of modifications at sites of interests, as well as subsequent energy minimization. Finally, the server makes available force field parameters and input files needed to run MD simulations of modified proteins within the framework of the widely used GROMOS 54A7 and 45A3 force fields and GROMACS simulation package.



**HOW TO USE VIENNA PTM**

Entrypoint:

.. code-block:: python

   # 1. Activate conda environment
   conda activate viennaptm

   # 2. Use entrypoint to run ViennaPTM
   viennaptm --input tests/data/1vii.pdb \
             --modification "A:50=V3H" \
             --output_pdb testoutput.pdb



API:

.. code-block:: python

   modifier = Modifier()
   structure = modifier.apply_modification(structure=structure,
                                           chain_identifier='A',
                                           residue_number=50,
                                           target_abbreviation="V3H")

