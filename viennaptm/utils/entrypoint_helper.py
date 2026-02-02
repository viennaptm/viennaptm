
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