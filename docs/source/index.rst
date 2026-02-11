ViennaPTM package
=================

.. toctree::
   :maxdepth: 7

   introduction
   installation
   tutorial
   list_of_ptms
   entrypoint
   api
   citation


Datastructures
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :caption: Datastructures

   ~dataclasses.annotatedstructure.AnnotatedStructure


Modifier
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :caption: Modifier

   ~modification.application.modifier.Modifier
   ~modification.modification_library.AddBranch
   ~modification.modification_library.Modification
   ~modification.modification_library.ModificationLibraryMetadata
   ~modification.modification_library.ModificationLibrary
   ~entrypoints.viennaptm.ModifierParameters
   ~utils.visualizer.Visualizer


GROMACS
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :caption: GROMACS

   ~gromacs.editconf.EditConf
   ~gromacs.gromacs_command.GromacsCommand
   ~gromacs.grompp.Grompp
   ~gromacs.pdb2gmx.PDB2GMXParameters
   ~gromacs.pdb2gmx.PDB2GMX
   ~gromacs.mdrun.Mdrun
   ~gromacs.trjconv.Trjconv

Miscellaneous
---

.. currentmodule:: viennaptm

.. autosummary::
   :toctree: generated/
   :template: functions
   :caption: Miscellaneous

   ~modification.calculation.align.compute_alignment_transform
   ~modification.calculation.align.apply_transform
   ~gromacs.minimization_pipeline.minimize_and_write_pdb
