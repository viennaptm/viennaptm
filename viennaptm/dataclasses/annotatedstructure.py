import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Union

import pandas as pd

from Bio.PDB import PDBIO, PDBParser, PDBList
from Bio.PDB.Structure import Structure

from viennaptm.utils.error_handling import raise_with_logging_error
from viennaptm.utils.files import log_writeout

logger = logging.getLogger(__name__)


class AnnotatedStructure(Structure):
    """Annotates structure of the ``biopython Structure`` class. Log administration as well as adding of new modifications.
    PDB's can be loaded from database or a file and annotated structures can be saved in a PDB file.
    """

    def __init__(self, id):
        Structure.__init__(self, id)
        self._init_calls()


    def _init_calls(self):
        self.modification_log = pd.DataFrame(columns=["residue_number", "chain_identifier",
                                                      "target_abbreviation", "modification_name"])

    def add_to_modification_log(self, residue_number: int, chain_identifier: str,
                                target_abbreviation: str, modification_name: str):
        """Adds modification of atoms to modification_log.

        :param residue_number: A residue number indicates the position of an amino acid in a protein's
        polypeptide chain, starting from \(1\) at the N-terminus and ending at the C-terminus. For example,
        ``"His 18"`` means the 18th amino acid in the chain is Histidine.
        :type residue_number: int
        .
        :param chain_identifier: Peptide or protein chain ID for instances of chains - commonly 1 capital letter.
        :type chain_identifier: str
        .
        :param target_abbreviation: A target abbreviation for a canonical protein refers to a standardized
        abbreviation for a standard, representative amino acid in a database like ``UniProt`` eg: ``ASP`` for Aspartic acid
        or ``GLU`` for Glutamic acid.
        :type target_abbreviation: str
        .
        :param modification_name: Protein modification refers to changes made to proteins after they are synthesized,
        with common types including glycosylation, phosphorylation, acetylation, ubiquitination, and methylation.
        These processes, often called post-translational modifications (PTMs), attach functional groups to a
        protein, altering its function and regulating cellular processes.
        :type modification_name: str
        """
        self.modification_log.loc[len(self.modification_log)] = [residue_number, chain_identifier,
                                                                 target_abbreviation, modification_name]
        ###TODO set modification input to user input

    def get_log(self) -> pd.DataFrame:
        """Accesses and returns modification log.

        :return: modification_log
        :rtype: pd.DataFrame
        """
        return self.modification_log

    def print_log(self):
        """Removes the index from the modification log and then prints the log. Even long (max. columns 1000) and
        wide (width 1000) data frames are printable.
        """

        # settings allow printing of long and wide dataframes
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_columns', 1000)

        # removes index
        blankIndex = [''] * len(self.modification_log)
        self.modification_log.index = blankIndex

        # adds a line for better visibility
        print('\n')
        print(self.modification_log)

    def delete_log_entry(self, residue_number: int, chain_identifier: str,):
        """Deletes a log entry according to residue_number and chain_identifier.

        :param residue_number: A residue number indicates the position of an amino acid in a protein's
        polypeptide chain, starting from \(1\) at the N-terminus and ending at the C-terminus. For example,
        ``"His 18"`` means the 18th amino acid in the chain is Histidine.
        :type residue_number: int
        .
        :param chain_identifier: Petite or protein chain ID for instances of chains - commonly 1 capital letter.
        :type chain_identifier: str
        """

        self.modification_log.drop(self.modification_log[(self.modification_log["residue_number"] == residue_number)&
                                                         (self.modification_log["chain_identifier"] == chain_identifier)].index,
                                    inplace=True)

    @classmethod
    def from_pdb_db(cls, identifier: str):
        """Loads structure from 'PDB database <https://www.rcsb.org/>'.

        :param identifier: Identifier string of length four.
        :type identifier: str
        ...
        :raises AttributeError: Raises an error when the parameter identifier string has not a length of four.
        :raises FileExistsError: Raises an error when file cannot be accessed from given path.
        ...
        :return: Returns a ``biopython PDB structure``.
        :rtype: AnnotatedStructure
        """
        if not isinstance(identifier, str) or len(identifier) != 4:
            raise_with_logging_error("Parameter identifier required to be a string of length four.",
                                    logger=logger,
                                    exception_type=AttributeError)

        # download the file; store it in a local copy (to provide identical results to "from_pdb_file()"
        downloader = PDBList()
        tmp_folder = tempfile.mkdtemp()
        path = downloader.retrieve_pdb_file(pdb_code=identifier, pdir=tmp_folder, file_format="pdb")
        logger.debug(f"Wrote temporary PDB file: {path}")

        # check whether file exists (success) or not
        if not os.path.isfile(path):
            raise_with_logging_error(f"Structure with identifier {identifier} (attempted path: {path}) "
                                     f"could not be retrieved.",
                                     logger=logger,
                                     exception_type=FileExistsError)

        # load the file, clean it up and return structure
        annotated_structure = cls.from_pdb(path=path)
        shutil.rmtree(os.path.dirname(path))
        return annotated_structure

    @classmethod
    def from_pdb(cls, path: Union[str, Path]):
        """Loads a PDB structure from given path.

        :param path: Path to a local PDB file.
        :type path: str or Path object
        ...
        :raises TypeError: Raises error if given path is not a string or Path object.
        ...
        :return: Returns a ``biopython PDB structure``.
        :rtype: AnnotatedStructure
        """
        if not isinstance(path, str) and not isinstance(path, Path):
            raise_with_logging_error(f"Parameter path (attempted path: {path}) required to be a path "
                                     f"(as string or Path object) to a local PDB file.",
                                     logger=logger,
                                     exception_type=TypeError)

        # load the file and return structure
        parser = PDBParser()
        structure = parser.get_structure(id=os.path.basename(path), file=path)

        # caution: __init__() of AnnotatedStructure is not executed! Manually add attributes!
        structure.__class__ = AnnotatedStructure
        structure._init_calls()
        return structure

    def to_pdb(self, path: str) -> None:
        """Saves a ``biopython PDB structure`` to a given path.

        :param path: Path to save the PDB file.
        :type path: str
        """
        io = PDBIO()
        io.set_structure(self)
        io.save(file=path)
        log_writeout(logger=logger, path=path)
