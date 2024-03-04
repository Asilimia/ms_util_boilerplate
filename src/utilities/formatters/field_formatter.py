def format_dict_key_to_camel_case(dict_key: str) -> str:
    """
    The function `format_dict_key_to_camel_case` converts a string from snake case
    to camel case.

    :param dict_key: The `dict_key` parameter is a string representing a key in a
    dictionary
    :type dict_key: str
    :return: a string that is formatted in camel case.
    """
    return "".join(
        word if idx == 0 else word.capitalize()
        for idx, word in enumerate(dict_key.split("_"))
    )
