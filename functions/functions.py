"""Custom functions."""


def stringify_list(list_: list,
                   quoted: bool = False
                   ) -> str:
    """Converts a list to a string representation.

    Accepts a list of mixed data type objects and returns a string
    representation. Optionally enclosed each item in single-quotes.

    Args:
        list_: The list to convert to a string.
        quoted: Indicates if the items in the list should be in quotes.

    Returns:
        A string representation of the list.
    """
    if quoted:
        string_ = ', '.join(f"'{i}'" for i in list_)
    else:
        string_ = ', '.join(f'{i}' for i in list_)

    return string_
