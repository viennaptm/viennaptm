from xml.dom import minidom
from utils.move_directory_up import move_directory_up
import os

class IO_library:
    def __init__(self):
        pass

    def load_database(self, path=None):
        if path is None:
            # load the latest internal library
            print(__file__)
            path = os.path.join(move_directory_up(__file__),
                                "libraries")
            print(os.listdir(path))
            print(path)
        #xml_doc = minidom.parse(

        #items = mydoc.getElementsByTagName('item')

        # one specific item attribute
        #print('Item #2 attribute:')
        #print(items[1].attributes['name'].value)

        # all item attributes
        #print('\nAll attributes:')
        #for elem in items:
        #    print(elem.attributes['name'].value)

        # one specific item's data
        #print('\nItem #2 data:')
        #print(items[1].firstChild.data)
        #print(items[1].childNodes[0].data)

        # all items data
        #print('\nAll item data:')
        #for elem in items:
         #   print(elem.firstChild.data)