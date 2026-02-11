import logging
import re
import sys

from pathlib import Path

from viennaptm.dataclasses.annotatedstructure import AnnotatedStructure
from viennaptm.dataclasses.parameters.modifier_parameters import ModifierParameters
from viennaptm.gromacs.minimization_pipeline import execute_energy_minimization
from viennaptm.modification.application.modifier import Modifier
from viennaptm.utils.entrypoint_helper import collect_kwargs, expand_dotted_keys, print_help_CLI
from viennaptm.utils.logger import instantiate_logging_CLI

logger = logging.getLogger(__name__)


def main():
    """
    Entry point for the :class:`AnnotatedStructure` modification command-line interface.

    This tool:
    - Parses command-line arguments
    - Validates parameters using :class:`ModifierParameters`
    - Initializes logging
    - Loads a :class:`Biopython PDB structure` (local file or database)
    - Applies one or more residue modifications
    - (Optionally) Energy minimizes the structure using GROMACS
    - Writes the modified :class:`AnnotatedStructure` to a PDB file

    :raises ValueError:
        If modification strings do not conform to the expected format.
    """

    # if --help, -h, --version or -v is set, this will print the help message and
    # immediately end the execution
    print_help_CLI("viennaptm", sys.argv, ModifierParameters)

    # load and parse all input using the parameter model
    raw_kwargs = collect_kwargs(sys.argv)
    raw_kwargs = expand_dotted_keys(raw_kwargs)
    cfg = ModifierParameters(**raw_kwargs)

    # set up logging
    instantiate_logging_CLI(cfg=cfg, logger=logger)

    # load internal PDB file
    if isinstance(cfg.input, Path):
        structure = AnnotatedStructure.from_pdb(path=cfg.input)
    else:
        structure = AnnotatedStructure.from_rcsb(identifier=cfg.input)

    # initialize modifier with most recent internal modification database
    modifier = Modifier()
    modlist = cfg.modify
    if modlist:
        for mod_input in modlist:
            modification = (re.split(":|=", mod_input))
            if not len(modification[0]) == 1:
                raise ValueError(f"Modification input needs to be a string of format 'A:50=V3H' "
                                 f"with the chain identifier being a string of length 1.")

            # check, whether the second string element (residue number) can be cast to an integer
            _ = int(modification[1])

            if not len(modification[2]) == 3:
                raise ValueError(f"Modification input needs to be a string of format 'A:50=V3H' "
                                 f"with the target residue abbreviation being a string of length 3.")

            # apply a modification
            structure = modifier.modify(structure = structure,
                                        chain_identifier=modification[0],
                                        residue_number=int(modification[1]),
                                        target_abbreviation=modification[2])

            logger.debug(f"Modification with parameters: "
                         f"chain identifier {modification[0]}, "
                         f"residue number {modification[1]} and"
                         f"target abbreviation {modification[2]} has been successfully applied.")
    else:
        logger.warning(f"No modification input provided - skipping.")

    # execute energy minimization, if enabled
    if cfg.gromacs.minimize:
        logger.info(f"Begin energy minimization ...")
        structure = execute_energy_minimization(structure=structure)
        logger.info(f"Completed energy minimization.")

    # write modified file
    if str(cfg.output).endswith(".pdb"):
        structure.to_pdb(str(cfg.output))
    elif str(cfg.output).endswith(".cif"):
        structure.to_cif(str(cfg.output))
    else:
        raise ValueError(f"Output file format not recognized, needs to be \".pdb\" or \".cif\".")
    logger.debug(f"Wrote structure to file: {cfg.output}")

if __name__ == "__main__":
    main()
