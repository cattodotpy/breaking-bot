def format_number(number: float):
    return "{:,.2f}".format(number)


def denumerize(number_str: str) -> float:
    SUFFIXES = ["", "k", "m", "b", "t", "q", "qi", "sx", "sp", "o", "n", "d"]
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

def format_interval(seconds: int) -> str:
    INTERVALS = [
        ("year", 31536000),
        ("month", 2592000),
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    ]

    parts = []
    for name, duration in INTERVALS:
        if seconds >= duration:
            value = seconds // duration
            seconds %= duration
            parts.append(f"{value} {name}{'s' if value != 1 else ''}")

    return " and ".join(parts)