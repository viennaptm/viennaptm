# standard
from xml.dom import minidom
import os

# custom
from modification.modification import *
from modification.mod_library import ModLibrary
from utils.move_directory_up import move_directory_up


class IO_ModLibrary:
    def __init__(self):
        pass

    def load_database(self, path=None):
        """Function loads an input XML file and creates and returns modification entries in a library collection."""
        # load the latest internal library, if none has been specified explicitly
        if path is None:
            path = os.path.join(move_directory_up(__file__), "libraries")
            files = os.listdir(path)
            files = {x for x in files if x.endswith("_library.xml")}
            path = os.path.join(path, sorted(files, reverse=True)[0])

        # load the XML and initialize the modification library
        xml_lib = minidom.parse(path).getElementsByTagName("library")[0]
        libObj = ModLibrary(last_update_date=xml_lib.attributes["last_update"].value,
                            version=xml_lib.attributes["version"].value)

        # iterate over the modifications and residues and fill the library
        residues = xml_lib.getElementsByTagName("residue")
        for residue in residues:
            initial_abbreviation = residue.getAttribute("abbreviation").upper()
            initial_name = residue.getAttribute("name").lower()
            modifications = residue.getElementsByTagName("modification")
            for modi in modifications:
                modification_name = modi.getAttribute("name").upper()
                target_abbreviation = modi.getAttribute("target_abbreviation").upper()
                target_name = modi.getAttribute("target_name").lower()

                # get the anchor atom
                anchor = None
                try:
                    anchor = modi.getElementsByTagName("anchor")[0].firstChild.nodeValue.upper()
                except IndexError:
                    pass

                # get the relative coordinate axes
                axesDict = {}
                try:
                    axes = modi.getElementsByTagName("axes")[0].getElementsByTagName("axis")
                    for axis in axes:
                        key = "".join(["axis", axis.getAttribute("number")])
                        axesDict[key] = Axis(number=axis.getAttribute("number"),
                                             p1 = axis.getAttribute("p1").upper(),
                                             p2 = axis.getAttribute("p2").upper())
                except IndexError:
                    pass

                # get the atom additions
                atom_additions = []
                try:
                    additions = modi.getElementsByTagName("additions")[0].getElementsByTagName("add")
                    for addition in additions:
                        atom_additions.append(AtomAddition(name=addition.getAttribute("name").upper(),
                                                           eletype=addition.getAttribute("eletype").upper(),
                                                           xcoorr=addition.getAttribute("xcoorr"),
                                                           ycoorr=addition.getAttribute("ycoorr"),
                                                           zcoorr=addition.getAttribute("zcoorr"),
                                                           tempfactor=addition.getAttribute("tempfactor")))
                except IndexError:
                    pass

                # get the atom deletions
                atom_deletions = []
                try:
                    deletions = modi.getElementsByTagName("deletions")[0].getElementsByTagName("del")
                    for deletion in deletions:
                        atom_deletions.append(AtomDeletion(name=deletion.getAttribute("name").upper()))
                except IndexError:
                    pass

                # get the atom replacements
                atom_replacements = []
                try:
                    replacements = modi.getElementsByTagName("")[0]
                    for replacement in replacements:
                        new_eletype = None
                        if "new_eletype" in replacement.attrib:
                            new_eletype = replacement.getAttribute("new_eletype").upper()
                        atom_replacements.append(AtomReplacement(name=replacement.getAttribute("name").upper(),
                                                                 by=replacement.getAttribute("by").upper(),
                                                                 new_eletype=new_eletype))
                except IndexError:
                    pass

                new_modification = Modification(initial_abbreviation=initial_abbreviation,
                                                initial_name=initial_name,
                                                modification_name=modification_name,
                                                target_abbreviation=target_abbreviation,
                                                target_name=target_name,
                                                anchor=anchor,
                                                axis1=axesDict["axis1"],
                                                axis2=axesDict["axis2"],
                                                atom_additions=atom_additions,
                                                atom_deletions=atom_deletions,
                                                atom_replacements=atom_replacements)
                libObj.add_modification(new_modification)

        return libObj