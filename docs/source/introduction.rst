Introduction
============


.. rubric:: WHAT ARE PTMs?

Post-translational modifications (PTMs) are chemical changes that occur on proteins after
they have been synthesized by the ribosome. These modifications extend the functional
diversity of proteins beyond what is directly encoded in the amino-acid sequence.
From a chemical perspective, PTMs are covalent modifications of amino-acid side chains and,
in some cases, of the protein backbone or the N- and C-termini.
PTMs can affect key protein properties such as molecular mass, electric charge, three-dimensional
structure, stability and lifetime, cellular localization, and biological activity.


In cells, PTMs are introduced via two main mechanisms:

| • **Enzymatic PTMs** are installed by specific enzymes. They are usually tightly regulated,
|   site-specific, and often reversible.
| • **Non-enzymatic PTMs** occur without enzymatic control and are driven by intrinsic
|   chemical reactivity and cellular conditions such as pH, redox state, or metabolite
|   concentrations.


.. rubric:: WHY DO PTMs MATTER?

PTMs dramatically increase proteome complexity and enable rapid regulation of protein
function without the need for new protein synthesis, allowing a much larger set of building
blocks than what is provided by the 20 canonical amino acids. Through PTMs, a single protein
can adopt multiple functional states depending on the cellular context.

Cellular regulation relies heavily on PTMs because they:

| • enable fast and reversible decision-making
| • conserve cellular energy
| • ensure correct timing of biological processes
| • allow cellular and tissue specialization
| • prevent uncontrolled or damaging reactions

When regulatory mechanisms fail, normal cellular behavior breaks down and disease can
arise. As a result, PTMs play central roles in cancer, neurodegeneration, metabolic
disorders, and immune system function.


.. rubric:: WHAT DOES VIENNA-PTM DO?

`Vienna-PTM <https://doi.org/10.1093/nar/gkt416>`__ is a software tool developed in the
group of Prof. Bojan Žagrović at the
`MFPL Institute <https://www.maxperutzlabs.ac.at/research/research-groups/zagrovic>`__ of
the University of Vienna. It enables the automated and chemically realistic introduction
of PTMs into protein three-dimensional structures provided as PDB files.
Vienna-PTM currently supports 256 enzymatic and non-enzymatic PTMs and performs geometrically
accurate placement of modifications at user-defined sites (see :doc:`list_of_ptms` for a complete list).
Optionally, users can perform a subsequent energy minimization using the GROMACS molecular
simulation package. This removes unfavorable steric orientations and makes the structure
amenable to downstream processing.
Vienna-PTM is designed to support structural and computational applications,
such as molecular dynamics simulations and structural analysis. Force-field parameters are
provided for the widely used **GROMOS 45A3, 54A7, and 54A8** force fields, with direct
compatibility with GROMACS.


.. rubric:: LICENCE AND CONTRIBUTION

The `Vienna-PTM package <https://github.com/viennaptm/viennaptm>`__ is an open-source
project and is free to use. Users are encouraged to review the
`code <https://github.com/viennaptm/viennaptm/blob/development/LICENSE>`__ and
`library <https://github.com/viennaptm/viennaptm/blob/development/viennaptm/resources/LICENSE>`__
licences before using the software.

Contributions from the community are highly welcome. Please consult the
`contribution guidelines <https://github.com/viennaptm/viennaptm/blob/development/CONTRIBUTE.md>`__
before submitting changes, in order to help keep the code base maintainable, robust, and
efficient.
