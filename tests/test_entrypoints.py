import unittest

from pathlib import Path
from pydantic import ValidationError
from viennaptm.entrypoints.modifier import ModifierParameters

class TestEntrypoints(unittest.TestCase):
    def test_output_pdb(self):
        mv = ModifierParameters.model_validate({"input": Path('text.pdb'),
                                               "modification": ['C', 'O', "CB", "OD1", "ND2"],
                                               "output_pdb": Path('text.pdb')})
        self.assertEqual(mv.input.suffix, ".pdb")
        self.assertEqual(type(mv.modification), list)
        self.assertEqual(type(mv.modification[3]), str)
        self.assertEqual(mv.output_pdb.suffix,".pdb")

        # input file needs to be a path (type: Union[Path, str]), execution should fail otherwise
        with self.assertRaises(ValidationError):
            ModifierParameters.model_validate({"input": 2,
                                               "modification": ['C', 'O', "CB", "OD1", "ND2"],
                                               "output_pdb": Path('text.pdb')})

        # modification ending needs to be a list of strings, execution should fail otherwise
        with self.assertRaises(ValidationError):
            ModifierParameters.model_validate({"input": Path('text.pdb'),
                                               "modification": [2, 'O', "CB", "OD1", "ND2"],
                                               "output_pdb": Path('text.pdb')})

        # output file ending needs to be on ".pdb", execution should fail otherwise
        with self.assertRaises(ValidationError):
             ModifierParameters.model_validate({"input": Path('text.pdb'),
                                                "modification": ['C', 'O', "CB", "OD1", "ND2"],
                                                "output_pdb": Path('text.txt')})