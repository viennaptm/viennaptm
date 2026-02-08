import unittest

from pathlib import Path
from pydantic import ValidationError
from viennaptm.entrypoints.viennaptm import ModifierParameters


class TestEntrypoints(unittest.TestCase):
    def test_output_pdb(self):
        mv = ModifierParameters.model_validate({"input": Path('text.pdb'),
                                               "modify": ['C', 'O', "CB", "OD1", "ND2"],
                                               "output": Path('text.pdb')})
        self.assertEqual(mv.input.suffix, ".pdb")
        self.assertEqual(type(mv.modify), list)
        self.assertEqual(type(mv.modify[3]), str)
        self.assertEqual(mv.output.suffix, ".pdb")

        # input file needs to be a path (type: Union[Path, str]), execution should fail otherwise
        with self.assertRaises(ValidationError):
            ModifierParameters.model_validate({"input": 2,
                                               "modify": ['C', 'O', "CB", "OD1", "ND2"],
                                               "output": Path('text.pdb')})

        # modification ending needs to be a list of strings, execution should fail otherwise
        with self.assertRaises(ValidationError):
            ModifierParameters.model_validate({"input": Path('text.pdb'),
                                               "modify": [2, 'O', "CB", "OD1", "ND2"],
                                               "output": Path('text.pdb')})

        # output file ending needs to be on ".pdb", execution should fail otherwise
        with self.assertRaises(ValidationError):
             ModifierParameters.model_validate({"input": Path('text.pdb'),
                                                "modify": ['C', 'O', "CB", "OD1", "ND2"],
                                                "output": Path('text.txt')})