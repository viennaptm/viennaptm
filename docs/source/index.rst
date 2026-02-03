ViennaPTM package
=================

.. toctree::
   :maxdepth: 4

   introduction
   tutorial
   entrypoint
   api


Datastructures
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :caption: Datastructures

   dataclasses.annotatedstructure.AnnotatedStructure


Modifier
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :caption: Modifier

   modification.application.modifier.Modifier
   modification.modification_library.AddBranch
   modification.modification_library.Modification
   entrypoints.viennaptm.ModifierParameters


GROMACS
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :caption: GROMACS

   gromacs.editconf.EditConf
   gromacs.gromacs_command.GromacsCommand
   gromacs.grompp.Grompp
   gromacs.pdb2gmx.PDB2GMXParameters
   gromacs.pdb2gmx.PDB2GMX
   gromacs.mdrun.Mdrun
   gromacs.minimization_pipeline.minimize_and_write_pdb
   gromacs.trjconv.Trjconv

Miscellaneous
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :template: functions
   :caption: Miscellaneous

   modification.calculation.align.compute_alignment_transform
   modification.calculation.align.apply_transform
   utils.visualizer.Visualizer



See :cite:`Margreitter2013` for the `publication <https://doi.org/10.1093/nar/gkt416>`_.



.. bibliography:: references.bib