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


def check_dc_qim():
    values = [x for x in range(256)]

    for i in range(2, 12):
        print(f'delta: {i}')
        kw = {
            'delta': i,
            'alpha': 0.65
        }
        resp1 = alg.dc_qim([values, values, values], [0] * 256, **kw)
        resp2 = alg.dc_qim([values, values, values], [1] * 256, **kw)
        # resp3 = qim([values, values, values], [0] * 256)
        # resp4 = qim([values, values, values], [1] * 256)
        print([resp1[2][y] for y in range(256)])
        print([resp2[2][y] for y in range(256)])
        # print([resp3[2][y] for y in range(256)])
        # print([resp4[2][y] for y in range(256)])
        resp3 = list(alg.i_dc_qim(resp1, **kw)[2])  # lsb([values, values, values], [0] * 256)
        resp4 = list(alg.i_dc_qim(resp2, **kw)[2])  # lsb([values, values, values], [1] * 256)
        print(resp3)
        print(resp4)

