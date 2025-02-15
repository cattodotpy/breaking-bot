def format_number(number: float):
    return "{:,.2f}".format(number)


def denumerize(number_str: str) -> float:
    SUFFIXES = (
        "",
        "k",
        "m",
        "b",
        "t",
        "qa",
        "qu",
        "s",
        "oc",
        "no",
        "d",
        "ud",
        "dd",
        "td",
        "qt",
        "qi",
        "se",
        "od",
        "nd",
        "v",
        "uv",
        "dv",
        "tv",
        "qv",
        "qx",
        "sx",
        "ox",
        "nx",
        "tn",
        "x",
        "xx",
        "xxx",
        "end",
    )
    SUFFIX_TO_MULTIPLIER = {
        suffix: 10 ** (3 * index) for index, suffix in enumerate(SUFFIXES)
    }

    try:
        # Find where the numeric part ends and the suffix begins
        suffix_idx = next(
            (
                i
                for i, char in enumerate(number_str)
                if not (char.isdigit() or char == ".")
            ),
            len(number_str),
        )
        number_part = number_str[:suffix_idx]
        suffix_part = number_str[suffix_idx:].lower()

        if suffix_part not in SUFFIX_TO_MULTIPLIER:
            raise ValueError("Invalid suffix in number format.")

        return float(number_part) * SUFFIX_TO_MULTIPLIER[suffix_part]
    except ValueError as e:
        raise ValueError("Invalid number format.") from e
