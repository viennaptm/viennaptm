import os
from xml.dom import minidom

from viennaptm.modification.modification import *
from viennaptm.modification.mod_library import ModLibrary
from viennaptm.utils.paths import move_directory_up

from viennaptm.utils.enums.io_enums import IOModificationEnum


class IOModLibrary:
    """Input / output class for modification XML libraries"""
    def __init__(self):
        self._IM = IOModificationEnum()

    def load_database(self, path=None):
        """Function loads an input XML file and creates and returns modification entries in a library collection."""
        # load the latest internal library, if none has been specified explicitly
        if path is None:
            path = os.path.join(move_directory_up(__file__), self._IM.INTERNAL_LIBRARY_PATH)
            files = os.listdir(path)
            files = {x for x in files if x.endswith(self._IM.INTERNAL_LIBRARY_SUFFIX)}
            path = os.path.join(path, sorted(files, reverse=True)[0])

        # load the XML and initialize the modification library
        xml_lib = minidom.parse(path).getElementsByTagName(self._IM.LIBRARY)[0]
        libObj = ModLibrary(last_update_date=xml_lib.attributes[self._IM.LIBRARY_LAST_UPDATE].value,
                            version=xml_lib.attributes[self._IM.LIBRARY_VERSION].value)

        # iterate over the modifications and residues and fill the library
        residues = xml_lib.getElementsByTagName(self._IM.RESIDUE)
        for residue in residues:
            initial_abbreviation = residue.getAttribute(self._IM.RESIDUE_ABBREVIATION).upper()
            initial_name = residue.getAttribute(self._IM.RESIDUE_NAME).lower()
            modifications = residue.getElementsByTagName(self._IM.MODIFICATION)
            for modification in modifications:
                modification_name = modification.getAttribute(self._IM.MODIFICATION_NAME).upper()
                target_abbreviation = modification.getAttribute(self._IM.TARGET_ABBREVIATION).upper()
                target_name = modification.getAttribute(self._IM.TARGET_NAME.lower())

                # get the anchor atom
                anchor = None
                try:
                    anchor = modification.getElementsByTagName(self._IM.ANCHOR)[0].firstChild.nodeValue.upper()
                except IndexError:
                    pass

                # get the relative coordinate axes
                axesDict = {}
                try:
                    axes = modification.getElementsByTagName(self._IM.AXES)[0].getElementsByTagName(self._IM.AXIS)
                    for axis in axes:
                        key = "".join([self._IM.AXIS, axis.getAttribute(self._IM.AXIS_NUMBER)])
                        axesDict[key] = Axis(number=axis.getAttribute(self._IM.AXIS_NUMBER),
                                             p1=axis.getAttribute(self._IM.AXIS_POINT1).upper(),
                                             p2=axis.getAttribute(self._IM.AXIS_POINT2).upper())
                except IndexError:
                    pass

                # get the three types of atom manipulations as lists
                atom_additions = self._get_atom_additions(modification=modification)
                atom_deletions = self._get_atom_deletions(modification=modification)
                atom_replacements = self._get_atom_replacements(modification=modification)

                new_modification = Modification(initial_abbreviation=initial_abbreviation,
                                                initial_name=initial_name,
                                                modification_name=modification_name,
                                                target_abbreviation=target_abbreviation,
                                                target_name=target_name,
                                                anchor=anchor,
                                                axis1=axesDict[self._IM.AXIS1],
                                                axis2=axesDict[self._IM.AXIS2],
                                                atom_additions=atom_additions,
                                                atom_deletions=atom_deletions,
                                                atom_replacements=atom_replacements)
                libObj.add_modification(new_modification)

        return libObj

    def _get_atom_additions(self, modification: minidom.Element) -> list:
        atom_additions = []
        try:
            additions = modification.getElementsByTagName(self._IM.ADDITIONS)[0].getElementsByTagName(self._IM.ADD)
            for addition in additions:
                atom_additions.append(AtomAddition(name=addition.getAttribute(self._IM.ADD_ATOM_NAME).upper(),
                                                   eletype=addition.getAttribute(self._IM.ADD_ATOM_ELETYPE).upper(),
                                                   xcoorr=addition.getAttribute(self._IM.ADD_ATOM_XCOORR),
                                                   ycoorr=addition.getAttribute(self._IM.ADD_ATOM_YCOORR),
                                                   zcoorr=addition.getAttribute(self._IM.ADD_ATOM_ZCOORR),
                                                   tempfactor=addition.getAttribute(self._IM.ADD_ATOM_TEMPFACTOR)))
        except IndexError:
            pass
        return atom_additions

    def _get_atom_deletions(self, modification: minidom.Element) -> list:
        atom_deletions = []
        try:
            deletions = modification.getElementsByTagName(self._IM.DELETIONS)[0].getElementsByTagName(self._IM.DEL)
            for deletion in deletions:
                atom_deletions.append(AtomDeletion(name=deletion.getAttribute(self._IM.DEL_ATOM_NAME).upper()))
        except IndexError:
            pass
        return atom_deletions

    def _get_atom_replacements(self, modification: minidom.Element) -> list:
        atom_replacements = []
        try:
            replacements = modification.getElementsByTagName(self._IM.REPLACEMENTS)[0].getElementsByTagName(self._IM.REP)
            for replacement in replacements:
                new_eletype = None

                # accessing attributes that are not present returns an empty string
                if replacement.getAttribute(self._IM.REP_NEW_ELETYPE) != "":
                    new_eletype = replacement.getAttribute(self._IM.REP_NEW_ELETYPE).upper()
                atom_replacements.append(AtomReplacement(name=replacement.getAttribute(self._IM.REP_ATOM_NAME).upper(),
                                                         by=replacement.getAttribute(self._IM.REP_BY_NAME).upper(),
                                                         new_eletype=new_eletype))
        except IndexError:
            pass
        return atom_replacements
