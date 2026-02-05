import json

from viennaptm.utils.fixtures import ViennaPTMFixtures

library_path = ViennaPTMFixtures().LATEST_PTMS_LIBRARY_PATH

with open(library_path) as f:
    library_dict = json.load(f)
    mapping_dict = {}

    for key in library_dict:
        ori_residue, mod_residue = key.split("_")
        if ori_residue not in mapping_dict:
            mapping_dict[ori_residue] = []

        # here we are sure that ori_residue is a key in mapping_dict
        # also, it will map to a list (empty or filled)
        assert(isinstance(mapping_dict[ori_residue], list))
        mapping_dict[ori_residue].append(mod_residue)
