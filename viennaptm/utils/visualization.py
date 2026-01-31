import nglview as nv
import os
import tempfile
from Bio.PDB import PDBIO
from copy import deepcopy

from typing import Union, Optional, Literal
from pydantic import BaseModel, field_validator

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure


class Visualization(BaseModel):
    structure: Union[AnnotatedStructure]
    name: Optional[Union[str]] = "structure"

    def show_structure_with_highlights(self,
                                       highlight_residues,
                                       cartoon_color="residueindex",
                                       save_html=True):
        # to avoid side-effects, duplicate structure
        structure = deepcopy(self.structure)

        # 1. Write PDB in temp_dir
        tmp_dir = tempfile.TemporaryDirectory()

        io = PDBIO()
        io.set_structure(structure)
        pdb_file = os.path.join(tmp_dir.name, f"{name}_temp.pdb")
        io.save(pdb_file)

        # 2. Load into NGL
        view = nv.show_file(pdb_file)
        view.clear()

        # 3. Add cartoon
        view.add_representation("cartoon", color=cartoon_color)

        # 4. Highlight residues reliably
        if highlight_residues:
            for chain_id, resnum in highlight_residues:
                # robust NGL selection syntax
                sele = f"chain {chain_id} and resid {resnum}"
                view.add_representation("ball+stick", selection=":".join([str(resnum), chain_id]), colorScheme="element")

        view.center()

        tmp_dir.cleanup()

        # 5. Save HTML (always works)
        if save_html:
            html_file = f"{name}.html"
            nv.write_html(html_file, view)
            print(f"Saved interactive view to: {html_file}")

        return view