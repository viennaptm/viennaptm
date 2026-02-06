API
============

.. rubric:: HOW TO LOAD A STRUCTURE?

The AnnotatedStructure class is an extension of :class:`Bio.PDB.Structure.Structure`.
This class adds logging functionality for residue-level modifications to a
:class:`Biopython PDB structure`. Structures can be loaded either from the RCSB
PDB database or from a local PDB file, annotated with modifications, and written
back to disk.

.. code-block:: python

    # Instantiate an `AnnotatedStructure` (base: :class:`Biopython PDB structure`)
    # with data from a local file.
    structure = AnnotatedStructure.from_rcsb("1vii")

    # Load a `AnnotatedStructure` (base: :class:`Biopython PDB structure`) from the
    # `RCSB PDB database <https://www.rcsb.org/>`_ via an identifier. Default format
    # has changed to mmcif.
    # The file is downloaded to a temporary directory, parsed, and then removed after loading.
    structure = AnnotatedStructure.from_pdb("1vii")


The application log is internally stored as a :class:`pandas.DataFrame` (and includes:
"residue_number", "chain_identifier", "original_abbreviation", "target_abbreviation").


The :class:`Modifier` class acts as a high-level interface between a
:class:`ModificationLibrary` and an annotated structure. It locates a
specific residue within a structure, removes hydrogen atoms from the target residue,
applies the requested modification using a template residue, and records the
modification in the structure's modification log.

.. code-block:: python

   # make an instance of the Modifier() class
   modifier = Modifier()


.. rubric:: HOW TO MODIFY A STRUCTURE?

The :py:meth:`Modifier.apply_modification` method locates a residue by chain identifier and residue number,
removes all hydrogen atoms, applies a modification defined in the modification library, and
optionally returns a modified copy of the structure.

.. code-block:: python

   # apply the modification to the modifier
   structure = modifier.apply_modification(structure=structure,
                                           chain_identifier='A',
                                           residue_number=50,
                                           target_abbreviation="V3H")


.. rubric:: HOW TO WRITE A STRUCTURE?

You can either write the ``AnnotatedStructure`` object (CAUTION: Only :class:`Biopython PDB
structure` elements) to a PDB file or a mmCIF file.


.. code-block:: python

    # writing the structure to a pdb file
    structure.to_pdb(tests/data/1vii.pdb)

    # writing the structure to a cif file
    structure.to_cif(tests/data/1vii.cif)


.. rubric:: HOW TO INSPECT A STRUCTURE?
You can inspect changes in the side-chains due to modifications by using the :class:Visualizer class.

.. code-block:: python

    # create a new Visualizer instance
    visualizer = Visualizer(structure=structure,
                            name="TestStructure")

    # call the visualization method and define the residues to be highlighted
    view = visualizer.render_view(highlight_residues=[("A", 50), ("A", 55), ("A", 60)])


    # you can either download the image as a PNG
    view.download_image(
                        filename="test.png",
                        factor=4,
                        transparent=False
    )


    # or export the view to HTML with the "save_html" parameter in the render call above
    view = visualizer.save_html

