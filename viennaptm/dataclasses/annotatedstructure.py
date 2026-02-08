import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Union

import pandas as pd

from Bio.PDB import PDBIO, PDBParser, PDBList, MMCIFIO
from Bio.PDB.Structure import Structure
from Bio.PDB.MMCIFParser import MMCIFParser

from viennaptm.utils.error_handling import raise_with_logging_error
from viennaptm.utils.files import log_writeout


logger = logging.getLogger(__name__)


class AnnotatedStructure(Structure):
    """
    Extension of :class:`Bio.PDB.Structure.Structure` with annotation support.

    This class adds logging functionality for residue-level modifications to a
    :class:`Biopython PDB structure`. Structures can be loaded either from the RCSB
    PDB database or from a local PDB file, annotated with modifications, and written
    back to disk.

    The application log is internally stored as a :class:`pandas.DataFrame`.
    """

    def __init__(self, id):
        """
        Initialize an :class:`AnnotatedStructure` instance.

        :param id: Identifier for the structure.
        :type id: str
        """

        Structure.__init__(self, id)
        self._init_calls()


    def _init_calls(self):
        """
        Initialize internal attributes.

        This method sets up the application log used to track residue
        modifications. It is called during normal initialization and must also
        be called manually when an existing :class:`Biopython structure` is cast to
        :class:`AnnotatedStructure`.
        """

        self.modification_log = pd.DataFrame(columns=["residue_number", "chain_identifier",
                                                      "original_abbreviation", "target_abbreviation"])

    def add_to_modification_log(self, residue_number: int,
                                chain_identifier: str,
                                original_abbreviation: str,
                                target_abbreviation: str):
        """
        Add a residue application entry to the application log.

        :param residue_number:
            Position of the residue in the polypeptide chain, starting at 1
            from the N-terminus. A residue number indicates the position of an amino acid
            in a protein's polypeptide chain, starting from \(1\) at the N-terminus and
            ending at the C-terminus. For example, ``"His 18"`` means the 18th amino acid
            in the chain is Histidine.
        :type residue_number: int

        :param chain_identifier:
            Chain identifier of the residue (commonly a single uppercase letter ).
        :type chain_identifier: str

        :param original_abbreviation:
            The original abbreviation for a canonical amino acid refers to a standardized
            three-letter abbreviation for a standard, representative amino acid in a database
            like ``UniProt`` eg: ``ASP`` for Aspartic acid or ``GLU`` for Glutamic acid.
        :type original_abbreviation: str

        :param target_abbreviation:
            Three-letter abbreviation of the modified or target amino acid.
        :type target_abbreviation: str
        """

        self.modification_log.loc[len(self.modification_log)] = [residue_number, chain_identifier,
                                                                 original_abbreviation, target_abbreviation]
        ###TODO set application input to user input

    def get_log(self) -> pd.DataFrame:
        """
        Return the application log.

        :return: DataFrame containing all logged residue modifications.
        :rtype: :class:`pandas.DataFrame`
        """

        return self.modification_log

    def print_log(self):
        """
        Print the application log to stdout.

        The index is removed prior to printing, and pandas display options
        are adjusted to allow printing of wide and long tables (max. columns 1000
        and max. width 1000).
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
        """
        Delete a application log entry.

        Entries are removed based on matching residue number and chain identifier.

        :param residue_number:
            Position of the residue in the polypeptide chain. A residue number indicates
            the position of an amino acid in a protein's polypeptide chain, starting
            from \(1\) at the N-terminus and ending at the C-terminus. For example,
            ``"His 18"`` means the 18th amino acid in the chain is Histidine.
        :type residue_number: int

        :param chain_identifier:
            Chain identifier of the residue.
        :type chain_identifier: str
        """

        self.modification_log.drop(self.modification_log[(self.modification_log["residue_number"] == residue_number)&
                                                         (self.modification_log["chain_identifier"] == chain_identifier)].index,
                                    inplace=True)

    @classmethod
    def from_rcsb(cls, identifier: str):
        """
        Load a `AnnotatedStructure` (base: :class:`Biopython PDB structure`) from the
        `RCSB PDB database <https://www.rcsb.org/>`_ via an identifier. Default format has changed to mmcif.

        The file is downloaded to a temporary directory, parsed, and then removed after loading.

        :param identifier:
            Four-character PDB identifier.
        :type identifier: str

        :raises AttributeError:
            If the identifier is not a string of length four.
        :raises FileExistsError:
            If the PDB file could not be retrieved.

        :return: Loaded and annotated structure.
        :rtype: :class:`AnnotatedStructure`
        """

        if not isinstance(identifier, str) or len(identifier) != 4:
            raise_with_logging_error("Parameter identifier required to be a string of length four.",
                                    logger=logger,
                                    exception_type=AttributeError)

        # download the file; store it in a local copy (to provide identical results to "from_pdb_file()"
        downloader = PDBList()
        tmp_folder = tempfile.mkdtemp()
        path = downloader.retrieve_pdb_file(pdb_code=identifier, pdir=tmp_folder, file_format="pdb")
        logger.debug(f"Wrote temporary file: {path}")

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
        """
        Instantiate an `AnnotatedStructure` (base: :class:`Biopython PDB structure`) with data from a local file.

        :param path:
            Path to the local PDB file.
        :type path: str or pathlib.Path

        :raises TypeError:
            If the path is not a string or Path object.

        :return: Loaded and annotated structure.
        :rtype: :class:`AnnotatedStructure`
        """

        if not isinstance(path, (str, Path)):
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

    @classmethod
    def from_cif(cls, path: Union[str, Path]):
        """
        Instantiate an `AnnotatedStructure` (base: :class:`Biopython PDB structure`) with data from a local file.

        :param path:
            Path to the local MMCIF file (ends on .cif).
        :type path: str or pathlib.Path

        :raises TypeError:
            If the path is not a string or Path object.

        :return: Loaded and annotated structure.
        :rtype: :class:`AnnotatedStructure`
        """

        if not isinstance(path, (str, Path)):
            raise_with_logging_error(f"Parameter path (attempted path: {path}) required to be a path "
                                     f"(as string or Path object) to a local MMCIF file.",
                                     logger=logger,
                                     exception_type=TypeError)

        # load the file and return structure
        parser = MMCIFParser()
        structure = parser.get_structure(structure_id=os.path.basename(path), filename=path)

        # caution: __init__() of AnnotatedStructure is not executed! Manually add attributes!
        structure.__class__ = AnnotatedStructure
        structure._init_calls()
        return structure

    def to_pdb(self, path: Union[str, Path]) -> None:
        """
        Write the ``AnnotatedStructure`` object (CAUTION: Only :class:`Biopython PDB structure` elements) to a PDB file.

        :param path:
            Destination path for the PDB file.
        :type path: str
        """

        io = PDBIO()
        io.set_structure(self)
        io.save(file=str(path))
        log_writeout(logger=logger, path=path)

    def to_cif(self, path: Union[str, Path]) -> None:
        """
        Write the ``AnnotatedStructure`` object (CAUTION: Only :class:`Biopython PDB structure` elements) to an mmCIF file.

        :param path:
            Destination path for the mmCIF file.
        :type path: str
        """
        io = MMCIFIO()
        io.set_structure(self)
        io.save(str(path))
        log_writeout(logger=logger, path=path)
