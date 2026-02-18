import sys
from typing import get_args, get_origin

from pydantic import BaseModel


def _add_value(kwargs: dict, key: str, value):
    """
    Add a value to a keyword-argument dictionary.

    If the key already exists, values are merged into a list. Existing
    scalar values are promoted to lists as needed. If the key does not
    exist, it is created.

    :param kwargs:
        Dictionary collecting parsed keyword arguments.
    :type kwargs: dict
    :param key:
        Argument name.
    :type key: str
    :param value:
        Value or list of values to associate with the key.
    :type value: Any
    """

    # Normalize to list internally
    if key in kwargs:
        if not isinstance(kwargs[key], list):
            kwargs[key] = [kwargs[key]]
        if isinstance(value, list):
            kwargs[key].extend(value)
        else:
            kwargs[key].append(value)
    else:
        kwargs[key] = value


def collect_kwargs(argv: list[str]) -> dict:
    """
    Parse command-line arguments into a keyword-argument dictionary.

    Supported argument forms include::

        --key=value
        --key value
        -key value
        --key v1 v2 v3
        -key v1 v2 v3
        repeated flags: --key v1 --key v2

    Parsing rules:

    * Flags start with ``--`` or ``-`` (excluding negative numbers).
    * After a flag, all consecutive non-flag tokens are interpreted
      as values for that flag.
    * Repeated flags accumulate values under the same key.

    :param argv:
        Command-line argument vector (typically ``sys.argv``).
    :type argv: list[str]
    :return:
        Dictionary mapping argument names to values or lists of values.
    :rtype: dict
    :raises ValueError:
        If a flag is missing required values or if an invalid argument
        format is encountered.
    """

    kwargs = {}
    i = 1

    def is_flag(token: str) -> bool:
        # Reject tokens like "-1" which might look like a negative number
        return token.startswith("--") or (token.startswith("-") and len(token) > 1 and not token[1].isdigit())

    while i < len(argv):
        arg = argv[i]

        # Case 1: --key=value
        if arg.startswith("--") and "=" in arg:
            key, value = arg[2:].split("=", 1)
            _add_value(kwargs, key, value)
            i += 1
            continue

        # Case 2: --key or -key
        if is_flag(arg):
            key = arg.lstrip("-")

            # Collect following non-flag tokens
            values = []
            j = i + 1
            while j < len(argv) and not is_flag(argv[j]):
                values.append(argv[j])
                j += 1

            if not values:
                raise ValueError(f"Missing value(s) for argument: {arg}")

            # If multiple tokens, treat as list
            if len(values) == 1:
                _add_value(kwargs, key, values[0])
            else:
                _add_value(kwargs, key, values)

            i = j
            continue

        raise ValueError(f"Invalid argument format: {arg}")

    return kwargs

def expand_dotted_keys(flat: dict) -> dict:
    # Pydantic does not expand things like "--gromacs.minimize" automatically,
    # so 'digest' them here and unpack as required
    out = {}
    for key, value in flat.items():
        parts = key.split(".")
        cur = out
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = value
    return out


def print_help_CLI(tool: str, argv: list[str], parameters_object):
    def is_basemodel_type(tp):
        origin = get_origin(tp)
        if origin is not None:
            tp = get_args(tp)[0]
        return isinstance(tp, type) and issubclass(tp, BaseModel)

    def get_basemodel_type(tp):
        origin = get_origin(tp)
        if origin is not None:
            return get_args(tp)[0]
        return tp

    def print_help(model: type[BaseModel], prefix=""):
        for name, field in model.model_fields.items():
            option = f"{prefix}{name}"
            annotation = field.annotation

            if is_basemodel_type(annotation):
                nested_model = get_basemodel_type(annotation)
                print_help(nested_model, option + ".")
                continue

            typ = getattr(annotation, "__name__", str(annotation))
            default = field.default
            desc = field.description or ""

            print(f"  --{option:<20} ")
            print(f"      [{typ}, default={default}]")
            if desc:
                print(f"      {desc}")

    if "--help" in argv or "-h" in argv or "--version" in argv or "-v" in argv:
        print("Usage:")
        print(f"  {tool} [OPTIONS]\n")
        print("Options:")
        print_help(parameters_object)
        sys.exit(0)
