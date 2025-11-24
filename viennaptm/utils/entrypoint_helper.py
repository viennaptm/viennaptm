
def _add_value(kwargs: dict, key: str, value):
    """
    Add a value or list of values under a given key. If the key exists, merge into a list, otherwise create the key.
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
    Supported forms:

        --key=value
        --key value
        -key value
        --key v1 v2 v3
        -key v1 v2 v3
        repeated flags: --key v1 --key v2

    Rules:
        After a flag, all consecutive non-flag tokens are values.
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