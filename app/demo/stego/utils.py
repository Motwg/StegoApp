import base64
from io import BytesIO
from PIL import Image


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


def encode_img(img, extension='PNG'):
    """
    Encodes pillow Image in base64
    :param img: pillow Image to encode
    :param extension: optional extension of image, PNG by default
    :return: base64 encoding
    """
    assert isinstance(img, Image.Image)
    file_object = BytesIO()
    img.save(file_object, extension)
    file_object.seek(0)
    b64 = base64.b64encode(file_object.getvalue()).decode('ascii')
    return f'data:image/png;base64,{b64}'


def decode_img(b64):
    """
    Decoded pillow Image from base64
    :param b64: encoded as base64 pillow Image
    :return: decoded pillow Image
    """
    x = str(b64).replace('data:image/png;base64,', '')
    x = base64.b64decode(x)
    return Image.open(BytesIO(x))
