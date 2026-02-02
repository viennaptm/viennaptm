from pathlib import Path

import nglview as nv
import os
import tempfile
from Bio.PDB import PDBIO
from copy import deepcopy

from typing import Union, Optional, Tuple, List
from pydantic import BaseModel, ConfigDict

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure


class Visualizer(BaseModel):
    """
    Interactive 3D visualization wrapper for biomolecular structures.

    This class provides a lightweight interface to render an
    :class:`~viennaptm.dataclasses.annotatedstructure.AnnotatedStructure`
    using `nglview <https://nglviewer.org/nglview/>`_. Structures are
    serialized to a temporary PDB file and displayed in a Jupyter-compatible
    interactive viewer.

    :param structure:
        Annotated structure to visualize.
    :type structure: AnnotatedStructure

    :param name:
        Base name used for temporary files and viewer identification.
    :type name: str, optional

    :param cartoon_color:
        Coloring scheme applied to the cartoon representation. This may be
        any valid NGL color scheme (e.g. ``"residueindex"``, ``"chainid"``,
        ``"element"``).
    :type cartoon_color: str, optional
    """

    structure: AnnotatedStructure
    name: Optional[str] = "structure"
    cartoon_color: Optional[str] = "residueindex"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def render_view(self,
                    highlight_residues: Optional[List[Tuple[str, str]]] = None,
                    save_html: Union[str, Path] = None):
        """
        Render the structure as an interactive NGLview widget.

        Optionally highlights specific residues using a ball-and-stick
        representation and can export the interactive view as a standalone
        HTML file.

        :param highlight_residues:
            List of residues to highlight, given as ``(chain_id, residue_number)``
            pairs. Highlighted residues are rendered using a ball-and-stick
            representation.
        :type highlight_residues: list[tuple[str, str]], optional

        :param save_html:
            Path to which the interactive viewer should be saved as an HTML
            file. If ``None``, no file is written.
        :type save_html: str or pathlib.Path, optional

        :returns:
            An NGLview widget displaying the structure.
        :rtype: nglview.NGLWidget
        """

        view = self._create_view(highlight_residues=highlight_residues)

        # using NGLview to generate PNGs etc. doesn't work, but HTML can be rendered out
        if save_html:
            nv.write_html(save_html, view)
            print(f"Saved interactive view to: {save_html}")

        return view

    def _create_view(self,
                     highlight_residues: Optional[List[Tuple[str, str]]] = None):
        """
        Create an NGLview widget from the stored structure.

        The structure is deep-copied to avoid side effects, written to a
        temporary PDB file, and then loaded into NGLview. The default
        representation is a cartoon, with optional ball-and-stick
        highlights for selected residues.

        :param highlight_residues:
            Residues to highlight, specified as ``(chain_id, residue_number)``
            pairs.
        :type highlight_residues: list[tuple[str, str]], optional

        :returns:
            Configured NGLview widget.
        :rtype: nglview.NGLWidget
        """

        # to avoid side-effects, duplicate structure
        structure = deepcopy(self.structure)

        # NGLview requires a temporary PDB file
        tmp_dir = tempfile.TemporaryDirectory()

        io = PDBIO()
        io.set_structure(structure)
        pdb_file = os.path.join(tmp_dir.name, f"{self.name}_temp.pdb")
        io.save(pdb_file)

        # load PDB file into NGLview
        view = nv.show_file(pdb_file)
        view.clear()

        # represent protein as cartoon
        view.add_representation("cartoon", color=self.cartoon_color)

        # selected residues are shown as balls and sticks
        if highlight_residues:
            for chain_id, resnum in highlight_residues:
                view.add_representation("ball+stick", selection=":".join([str(resnum), chain_id]), colorScheme="element")

        view.center()
        tmp_dir.cleanup()

        return view