import json
from pathlib import Path
from typing import Optional, Union, Dict, Any

import yaml
from pydantic import BaseModel, model_validator, field_validator, Field


class GROMACSParameters(BaseModel):
    minimize: bool = Field(default=False, description="Energy minimize the modified structure.")

    model_config = {
        "extra": "forbid"
    }


class ModifierParameters(BaseModel):
    """
    Configuration model for a Vienna-PTM command-line run.

    This Pydantic model represents the fully resolved configuration used by
    the Vienna-PTM CLI. Parameters can be provided either via command-line
    arguments or through an external YAML / JSON configuration file.

    Configuration resolution follows a strict precedence order:

    1. Values from the configuration file (``--config``) are loaded first.
    2. Explicit CLI arguments override values from the config file.
    3. The merged configuration is validated and normalized.

    Invalid or unknown parameters are rejected.

    Attributes
    ----------
    config : pathlib.Path or str, optional
        Path to a YAML or JSON configuration file.
    input : pathlib.Path or str, optional
        Input structure, either as a local PDB/mmCIF file or a 4-character
        PDB identifier.
    modify : list[str] or str, optional
        One or more residue modification specifications.
    output : pathlib.Path or str, optional
        Output structure file. Must end with ``.pdb`` or ``.cif``.
    logger : str
        Logging destination. Use ``"console"`` for stdout logging or a file
        path to enable file logging.
    debug : bool
        Enable verbose debug logging if ``True``.
    """

    config: Optional[Union[Path, str]] = Field(default=None, description="Path to a YAML or JSON configuration file (optional).")

    input: Optional[Union[Path, str]] = Field(default=None, description="Input structure, either CIF or PDB.")
    modify: Optional[Union[list[str], str]] = Field(default=None, description="Modifications in the form of \"A:50=V3H\", which means \"chain:residue=target\".")
    output: Optional[Union[Path, str]] = Field(default="output.pdb", description="Output structure, either CIF or PDB.")
    gromacs: Optional[GROMACSParameters] = Field(default_factory=GROMACSParameters, description="Gromacs parameters.")
    logger: Optional[str] = Field(default="console", description="Set logger to either console (default) or provide a file name.")
    debug: Optional[bool] = Field(default=False, description="If set to true, enable verbose debugging logging.")

    model_config = {
        "extra": "forbid"
    }

    def is_console_logging(self) -> bool:
        """
        Determine whether logging should be directed to the console.

        :returns:
            ``True`` if logging is configured for stdout, ``False`` if logging
            should be written to a file.
        :rtype: bool
        """

        return self.logger == "console"

    def log_file_path(self) -> Optional[Path]:
        """
        Return the log file path if file logging is enabled.

        When logging is set to ``"console"``, no log file is used and ``None``
        is returned. Otherwise, the value of :attr:`logger` is interpreted as
        a file path.

        :returns:
            Path to the log file, or ``None`` if console logging is enabled.
        :rtype: pathlib.Path or None
        """

        if self.is_console_logging():
            return None
        return Path(self.logger)

    @model_validator(mode="before")
    @classmethod
    def load_config_file(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load and merge a YAML or JSON configuration file.

        If a configuration file is specified via the ``config`` parameter, it
        is loaded first and used to initialize parameters. Any values provided
        directly (e.g. via CLI arguments) override those from the config file.

        :param values:
            Raw keyword arguments passed to the model constructor.
        :type values: dict

        :returns:
            Merged parameter dictionary with CLI values taking precedence.
        :rtype: dict

        :raises ValueError:
            If the config file does not exist, has an unsupported extension,
            or does not contain a top-level mapping.
        """

        config = values.get("config")
        if not config:
            return values

        config_path = Path(config)
        if not config_path.exists():
            raise ValueError(f"Config file does not exist: {config_path}.")

        if config_path.suffix in {".yaml", ".yml"}:
            with open(config_path, "r") as fh:
                config_data = yaml.safe_load(fh) or {}
        elif config_path.suffix == ".json":
            with open(config_path, "r") as fh:
                config_data = json.load(fh)
        else:
            raise ValueError("Config file must be YAML (.yaml/.yml) or JSON (.json).")

        if not isinstance(config_data, dict):
            raise ValueError("Config file must contain a mapping at the top level.")

        # CLI args override config file values (if present)
        return {**config_data, **values}

    @field_validator("output", mode="after")
    @classmethod
    def validate_output(cls, out: Union[Path, str]) -> Path:
        """
        Validate and normalize the output structure path.

        Ensures that the output filename ends with ``.pdb`` or ``.cif`` and
        converts string paths to :class:`pathlib.Path`.

        :param out:
            Output path or filename.
        :type out: pathlib.Path or str

        :returns:
            Validated output path.
        :rtype: pathlib.Path

        :raises ValueError:
            If the output file extension is not supported.
        """

        if isinstance(out, str):
            out = Path(out)

        if out.suffix not in {".pdb", ".cif"}:
            raise ValueError(
                'Output must be PDB / mmCIF format (ending must be ".pdb" or ".cif").'
            )
        return out

    @field_validator("modify", mode="after")
    @classmethod
    def validate_input_modification(
        cls, input_modification: Union[list[str], str]
    ) -> list[str]:
        """
        Normalize modification input to a list of strings.

        Single modification specifications are automatically wrapped into a
        list to ensure consistent downstream handling.

        :param input_modification:
            Modification specification(s).
        :type input_modification: str or list[str]

        :returns:
            List of modification strings.
        :rtype: list[str]
        """

        if isinstance(input_modification, str):
            input_modification = [input_modification]
        return input_modification

    @field_validator("input", mode="after")
    @classmethod
    def validate_file_input(cls, inp: Union[Path, str]):
        """
        Validate the input structure source.

        If the input is a string ending with ``.pdb`` or ``.cif``, it is treated
        as a local file path and converted to :class:`pathlib.Path`. Otherwise,
        it is interpreted as a PDB database identifier and must be exactly four
        characters long.

        :param inp:
            Input path or PDB identifier.
        :type inp: pathlib.Path or str

        :returns:
            Validated input value.
        :rtype: pathlib.Path or str

        :raises ValueError:
            If a non-file string input does not conform to the 4-character
            PDB identifier format.
        """

        if isinstance(inp, str):
            if inp.lower().endswith((".pdb", ".cif")):
                inp = Path(inp)
            else:
                if len(inp) != 4:
                    raise ValueError(
                        f"Database identifiers must be exactly 4 characters long. "
                        f"Input '{inp}' does not conform."
                    )
        return inp

    def dump_resolved_config(self) -> str:
        """
        Serialize the resolved configuration to YAML.

        All paths are converted to strings to ensure clean, human-readable
        output suitable for logging or inspection.

        :returns:
            YAML-formatted configuration string.
        :rtype: str
        """

        data = self.model_dump()

        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)

        return yaml.safe_dump(data, sort_keys=False)
