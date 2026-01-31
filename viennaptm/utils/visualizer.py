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
    structure: AnnotatedStructure
    name: Optional[str] = "structure"
    cartoon_color: Optional[str] = "residueindex"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def render_view(self,
                    highlight_residues: Optional[List[Tuple[str, str]]] = None,
                    save_html: Union[str, Path] = None):
        view = self._create_view(highlight_residues=highlight_residues)

        # using NGLview to generate PNGs etc. doesn't work, but HTML can be rendered out
        if save_html:
            nv.write_html(save_html, view)
            print(f"Saved interactive view to: {save_html}")

        return view

    def _create_view(self,
                     highlight_residues: Optional[List[Tuple[str, str]]] = None):
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