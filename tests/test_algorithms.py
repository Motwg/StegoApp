import numpy as np
from PIL import Image

from app.demo.stego import algorithms as alg


def test_correct_image_exists(image):
    assert isinstance(image, Image.Image)
    assert len(image.size) == 2
    assert image.size[0] > 0
    assert image.size[1] > 0


def test_lsb_without_watermark(image):
    assert isinstance(image, Image.Image)
    stego = alg.lsb(image, [])
    print(np.asarray(stego))
    assert isinstance(stego, Image.Image)


def test_lsb_with_watermark(image, b_watermark):
    assert isinstance(image, Image.Image)
    stego = alg.lsb(image, b_watermark)
    print(np.asarray(stego))
    assert isinstance(stego, Image.Image)


def test_qim_without_watermark(image):
    assert isinstance(image, Image.Image)
    stego = alg.qim(image, [])
    print(np.asarray(stego))
    assert isinstance(stego, Image.Image)


def test_qim_with_watermark(image, b_watermark):
    assert isinstance(image, Image.Image)
    stego = alg.qim(image, b_watermark)
    print(np.asarray(stego))
    assert isinstance(stego, Image.Image)


def test_dc_qim_without_watermark(image):
    assert isinstance(image, Image.Image)
    stego = alg.dc_qim(image, [])
    print(np.asarray(stego))
    assert isinstance(stego, Image.Image)


def test_dc_qim_with_watermark(image, b_watermark):
    assert isinstance(image, Image.Image)
    stego = alg.dc_qim(image, b_watermark)
    print(np.asarray(stego))
    assert isinstance(stego, Image.Image)

