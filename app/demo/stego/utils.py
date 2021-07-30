

def switch(switcher, case, default=None):
    """
    :param switcher: any callable which returns tuple: (dictionary from which to chose the case, default case)
           e.g. algorithm_switcher
    :param case: chosen case
    :param default: optional parameter to change default case
    :return: chosen in case element/s
    """
    assert callable(switcher)
    if default:
        return switcher()[0].get(case, default)
    else:
        dictionary, switcher_default = switcher()
        return dictionary.get(case, dictionary.get(switcher_default))


def str_to_binary(string):
    """
    :param string: any string
    :return: binary representation of string as list
    """
    bits = ''.join([f'{char:08b}' for char in bytearray(string, 'utf-8')])
    return [*map(int, list(bits))]
