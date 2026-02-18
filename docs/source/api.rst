API
============

.. rubric:: HOW TO LOAD A STRUCTURE?

The ``AnnotatedStructure`` class is an extension of
:class:`Bio.PDB.Structure.Structure`. It adds logging functionality for
residue-level modifications to a :class:`Biopython PDB structure`.

Structures can be loaded either from the RCSB PDB database or from a local PDB
file, annotated with modifications, and written back to disk.

.. code-block:: python

    # Instantiate an `AnnotatedStructure` from data stored in the RCSB PDB.
    structure = AnnotatedStructure.from_rcsb("1vii")

    # Load an `AnnotatedStructure` from a local PDB file.
    # The default file format has changed to mmCIF.
    # The file is downloaded to a temporary directory, parsed,
    # and removed after loading.
    structure = AnnotatedStructure.from_pdb("/path/to/1vii.pdb")


The application log is internally stored as a :class:`pandas.DataFrame` and
includes the following columns:

 *  ``residue_number``
 *  ``chain_identifier``
 *  ``original_abbreviation``
 *  ``target_abbreviation``


The :class:`Modifier` class acts as a high-level interface between a
:class:`ModificationLibrary` and an annotated structure. It locates a specific
residue within the structure, removes hydrogen atoms from the target residue,
applies the requested modification using a template residue, and records the
modification in the structure’s modification log.

.. code-block:: python

    # Create an instance of the Modifier class
    modifier = Modifier()


.. rubric:: HOW TO MODIFY A STRUCTURE?

The :py:meth:`Modifier.modify` method locates a residue by its chain identifier
and residue number, removes all hydrogen atoms, applies a modification defined
in the modification library, and returns a modified copy of the
structure. Optionally, use the ``inplace`` parameter to directly modify the input
structure.

.. code-block:: python

    # Apply a modification to the structure
    structure = modifier.modify(
        structure=structure,
        chain_identifier="A",
        residue_number=50,
        target_abbreviation="V3H"
    )


.. rubric:: HOW TO WRITE A STRUCTURE?

You can write an ``AnnotatedStructure`` object to either a PDB or an mmCIF file.
Note that only elements supported by the underlying
:class:`Biopython PDB structure` are written.

.. code-block:: python

    # Write the structure to a PDB file
    structure.to_pdb("tests/data/1vii.pdb")

    # Write the structure to an mmCIF file
    structure.to_cif("tests/data/1vii.cif")


.. rubric:: HOW TO INSPECT A STRUCTURE?

You can inspect side-chain changes resulting from modifications using the
:class:`Visualizer` class.

.. code-block:: python

    # Create a new Visualizer instance
    visualizer = Visualizer(
        structure=structure,
        name="TestStructure"
    )

    # Render the structure and highlight selected residues
    view = visualizer.render_view(
        highlight_residues=[("A", 50), ("A", 55), ("A", 60)]
    )

    # Download the rendered view as a PNG image
    view.download_image(
        filename="test.png",
        factor=4,
        transparent=False
    )

    # Alternatively, export the view to HTML
    view = visualizer.save_html
