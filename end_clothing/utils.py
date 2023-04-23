def parse_sizes(sizes):
    """
    This function takes an argument called 'sizes' and checks whether it is a list or not. If 'sizes' is not a list, it is converted to a list with the original value as its only element. The function then returns the resulting list.
    :param sizes: string or a list object
    :return: list of strings
    """
    if not isinstance(sizes, list):
        sizes = [sizes]
    return sizes
