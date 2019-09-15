# standard
from xml.dom import minidom
import os

# custom
from modification.modification import *
from modification.mod_library import ModLibrary
from utils.move_directory_up import move_directory_up


class IO_library:
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
            initial_abbreviation = residue["abbreviation"].value.upper()
            initial_name = residue["name"].value.lower()
            modifications = residue.getElementsByTagName("modification")
            for modi in modifications:
                modification_name = modi["name"].value.upper()
                target_abbreviation = modi["target_abbreviation"].upper()
                target_name = modi["target_name"].lower()
                anchor = modi.getElementsByName("anchor")[0].value.upper()

                # get the relative coordinate axes
                axes = modi.getElementsByName("axes")[0]
                axesDict = {}
                for axis in axes:
                    key = "".join(["axis", axis["number"].value])
                    axesDict = {key: Axis(number=axis["number"].value,
                                          p1 = axis["p1"].value.upper(),
                                          p2 = axis["p2"].value.upper())}

                # get the atom additions
                additions = modi.getElementsByName("additions")[0].getElementsByName("add")
                atom_additions = []
                for addition in additions:
                    atom_additions.append(AtomAddition(name=addition["name"].value.upper(),
                                                       eletype=addition["eletype"].value.upper(),
                                                       xcoorr=addition["xcoorr"].value,
                                                       ycoorr=addition["ycoorr"].value,
                                                       zcoorr=addition["zcoorr"].value,
                                                       tempfactor=addition["tempfactor"]))

                # get the atom deletions
                deletions = modi.getElementsByName("deletions")[0].getElementsByName("del")
                atom_deletions = []
                for deletion in deletions:
                    atom_deletions.append(AtomDeletion(name=deletion["name"].value.upper()))

                # get the atom replacements
                replacements = modi.getElementsByName("")[0]
                atom_replacements = []
                for replacement in replacements:
                    # TODO: new eletype?
                    pass
                    #atom_replacements.append(AtomReplacement(

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