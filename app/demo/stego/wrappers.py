from PIL import Image
import numpy as np
from functools import wraps

from .progress_callback import ProgressCallback


# allows using parameters in wrappers
def parametrised(dec):
    def wrapper(*args, **kwargs):
        def resp(f):
            return dec(f, *args, **kwargs)

        return resp

    return wrapper


@parametrised
def algorithm_wrapper(alg, domain_fit=False):
    @wraps(alg)
    def wrapper(img, watermark, *args, **kwargs):
        no_channels = kwargs.get('no_channels', 3)
        channel = kwargs.get('channel', [2])

        pixels = img
        if isinstance(img, Image.Image):
            pixels = image_to_pixels(img, no_channels)

        if domain_fit:
            delta = kwargs.get('delta', 3)
            domain = (0 + delta - 1, 255 - delta + 1)
            pixels = fit_domain(pixels, channel, domain)

        channel_size = len(pixels[channel[0]])
        watermark = fill_watermark(watermark, channel_size)
        watermarked = alg(pixels, watermark, *args, **kwargs)

        # change back to image if input (img) was image
        if isinstance(img, Image.Image):
            watermarked = pixels_to_image(watermarked, no_channels, img)
        return watermarked

    return wrapper


def i_algorithm_wrapper(alg):
    @wraps(alg)
    def wrapper(img, watermark=None, *args, **kwargs):
        no_channels = kwargs.get('no_channels', 3)
        channel = kwargs.get('channel', [2])

        pixels = img
        if isinstance(img, Image.Image):
            pixels = image_to_pixels(img, no_channels)

        message = alg(pixels, watermark, *args, **kwargs)
        if isinstance(img, Image.Image):
            byte_arr = pixels_to_bytes(message, channel)
            byte_arr = cut_bytes(byte_arr)
            message = bytes_to_utf8(byte_arr)
        return message

    return wrapper


def generate(generator):
    @wraps(generator)
    def wrapper(pixels, watermark=None, *args, **kwargs):
        assert hasattr(pixels, '__iter__')
        # default RGB Blue channel
        channels = kwargs.get('channel', [2])

        # Progress callback is available
        if len(args) > 0:
            if isinstance(cb := args[-1], ProgressCallback):
                for ch in channels:
                    cb.add_max_value(len(pixels[ch]))

                for ch in channels:
                    arr = []
                    for p in generator(pixels[ch], watermark, *args, **kwargs):
                        arr.append(p)
                        cb.add_current_value(1)
                    pixels[ch] = np.array(arr)
                return pixels

        # Progress callback is not available
        for ch in channels:
            pixels[ch] = np.array([x for x in generator(pixels[ch], watermark, *args, **kwargs)])
        return pixels

    return wrapper


def image_to_pixels(img, no_channels):
    assert isinstance(img, Image.Image)
    pixels = np.asarray(img)
    # shape: ((r, g, b) x pixels) => pixels grouped by channel ((r x pixels), (g x pixels), (b x pixels))
    try:
        pixels = np.array(pixels).reshape((img.size[1] * img.size[0], no_channels)).transpose()
    except ValueError:
        pixels = np.array(pixels).reshape((img.size[1], no_channels)).transpose()
    return pixels


def pixels_to_image(pixels, no_channels, img):
    # shape: ((r, g, b) x pixels) <= pixels grouped by channel ((r x pixels), (g x pixels), (b x pixels))
    if isinstance(img, Image.Image):
        pixels = np.array(pixels).transpose().reshape(img.size[1], img.size[0], no_channels)
    else:
        pixels = np.array(pixels).transpose().reshape(len(img[0]), no_channels)
    return Image.fromarray(pixels)


def pixels_to_bytes(pixels, channel):
    bits = pixels[channel[0]]
    # 8bit segments to bytes
    byte_arr = [(x := 0,
                 [x := 2 * x + p for p in bits[i:i + 8]][-1])[1]
                for i in range(0, len(bits), 8)]
    return [*map(int, byte_arr)]


def bytes_to_utf8(byte_arr):
    return bytearray(byte_arr).decode('utf-8', 'ignore')


def fill_watermark(watermark, channel_size):
    # repeat watermark
    if len(watermark) > 0:
        while channel_size > len(watermark) * 2:
            watermark = watermark * 2

    # fill watermark with 0
    while channel_size > len(watermark):
        watermark.append(0)
    return watermark


def cut_bytes(byte_arr):
    # cut zeros due to watermark filling
    assert isinstance(byte_arr, list)
    try:
        while byte_arr[-1] == 0:
            byte_arr.pop()
            # if popped all values throws IndexError
        return byte_arr
    except IndexError:
        return []


def fit_domain(pixels, channels, domain):
    pixels = np.array(pixels)
    for ch in channels:
        np.clip(pixels[ch], domain[0], domain[1], pixels[ch])
    return pixels
