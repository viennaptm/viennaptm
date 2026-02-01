import json
from pathlib import Path
from typing import Optional, Union, Dict, Any

import yaml
from pydantic import BaseModel, model_validator, field_validator


class ModifierParameters(BaseModel):
    """
    Pydantic model defining configuration parameters for a Vienna-PTM run.

    Parameters may be supplied either:
      - Directly via CLI arguments, or
      - via a YAML / JSON configuration file specified with ``--config``.

    Resolution rules:
      - The config file initializes parameters.
      - Explicit CLI arguments override config values.
      - All values are validated after merging.
    """

    config: Optional[Union[Path, str]] = None

    input: Optional[Union[Path, str]] = None
    modification: Optional[Union[list[str], str]] = None
    output_pdb: Optional[Union[Path, str]] = "output.pdb"
    logger: str = "console"
    debug: bool = False

    model_config = {
        "extra": "forbid"
    }

    def is_console_logging(self) -> bool:
        """
        Return True if logging should go to the console.
        """
        return self.logger == "console"

    def log_file_path(self) -> Optional[Path]:
        """
        Return the log file path if file logging is enabled, else None.
        """
        if self.is_console_logging():
            return None
        return Path(self.logger)

    @model_validator(mode="before")
    @classmethod
    def load_config_file(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load parameters from a YAML or JSON config file if provided.

        The config file is loaded first, then supplied keyword arguments
        (if any) override values from the configuration.

        :param values: Raw keyword arguments passed to the entrypoint.
        :return: Merged parameter dictionary.
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

    @field_validator("output_pdb", mode="after")
    @classmethod
    def validate_output_pdb(cls, out: Union[Path, str]) -> Path:
        """
        Validate the output PDB / mmCIF path.

        Ensures that the output filename ends with ``.pdb`` or ``.cif`` and
        converts string paths to :class:`pathlib.Path`.

        :param out: Output path or filename.
        :return: Validated output path.
        """
        if isinstance(out, str):
            out = Path(out)

        if out.suffix not in {".pdb", ".cif"}:
            raise ValueError(
                'Output must be PDB / mmCIF format (ending must be ".pdb" or ".cif").'
            )
        return out

    @field_validator("modification", mode="after")
    @classmethod
    def validate_input_modification(
        cls, input_modification: Union[list[str], str]
    ) -> list[str]:
        """
        Normalize modification input to a list of strings.

        Single modification strings are wrapped into a list to ensure
        consistent downstream handling.

        :param input_modification: Modification or list of modifications.
        :return: List of modification strings.
        """
        if isinstance(input_modification, str):
            input_modification = [input_modification]
        return input_modification

    @field_validator("input", mode="after")
    @classmethod
    def validate_file_input(cls, inp: Union[Path, str]):
        """
        Validate the input structure source.

        If the input is a string ending with ``.pdb`` or ``.cif``, it is
        interpreted as a file path and converted to :class:`pathlib.Path`.
        Otherwise, it is treated as a PDB database identifier and must be
        exactly four characters long.

        :param inp: Input path or PDB identifier.
        :return: Validated input value.
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
        Dump the fully resolved and validated configuration as a YAML string.

        :return: YAML-formatted configuration.
        """
        data = self.model_dump()

        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)

        return yaml.safe_dump(data, sort_keys=False)
