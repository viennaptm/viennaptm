import unittest

from viennaptm.io.modlibrary import IOModLibrary


class Test_IOModLibrary(unittest.TestCase):

    def test_loading(self):
        # load standard, internal database
        io_lib = IOModLibrary()
        lib = io_lib.load_database()

        # check proper loading
        self.assertEqual(len(lib), 121)
