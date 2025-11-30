import unittest
from viennaptm.modification.modification_dto import Modifications


class Test_Resources(unittest.TestCase):

    def test_library_loading(self):
        # load standard, internal database
        modifications = Modifications()

        # TODO: Check both indexing with integers and a tuple
        print(modifications[0])
        print(modifications["ARG", "RMN"])
