import numpy as np

from app.demo.stego import wrappers as wr


@wr.algorithm_wrapper()
@wr.generate
def lsb(pixels, watermark, *args, **kwargs):
    def generator():
        for x, y in zip(pixels, watermark):
            if y == 0:
                yield int(x) >> 1 << 1
            elif y == 1:
                yield (int(x) >> 1 << 1) + 1
            else:
                raise Exception('Wrong watermark')

    return generator()


@wr.i_algorithm_wrapper
@wr.generate
def i_lsb(pixels, *args, **kwargs):
    def generator():
        for p in pixels:
            yield p % 2

    return generator()


@wr.algorithm_wrapper(domain_fit=True)
@wr.generate
def qim(pixels, d_watermark, *args, **kwargs):
    delta = kwargs.get('delta', 3)

    def generator():
        for k, w in zip(pixels, d_watermark):
            yield np.round(k / delta) * delta - (-1) ** w * delta / 4

    return generator()


@wr.i_algorithm_wrapper
@wr.generate
def i_qim(watermarked, *args, **kwargs):
    delta = kwargs.get('delta', 3)

    def generator():
        for z in watermarked:
            z0 = np.round(z / delta) * delta - (-1) ** 0 * delta / 4
            z1 = np.round(z / delta) * delta - (-1) ** 1 * delta / 4
            d0 = np.abs(z - z0)
            d1 = np.abs(z - z1)
            if d0 < d1:
                yield 0
            else:
                yield 1
    return generator()


@wr.algorithm_wrapper(domain_fit=True)
@wr.generate
def dc_qim(pixels, watermark, *args, **kwargs):
    delta = kwargs.get('delta', 5)
    alpha = kwargs.get('alpha', 0.95)

    def q(x, w, d):
        return np.round(x / d) * d - (-1) ** w * d / 4

    def generator():
        for x, w in zip(pixels, watermark):
            x1 = q(x, w, delta / alpha)
            yield x1 + (1 - alpha) * (x - x1)

    return generator()


@wr.i_algorithm_wrapper
@wr.generate
def i_dc_qim(watermarked, *args, **kwargs):
    delta = kwargs.get('delta', 5)
    alpha = kwargs.get('alpha', 0.95)

    def q(x, w, d):
        return np.round(x / d) * d - (-1) ** w * d / 4

    def f(x, w, d, a):
        x1 = q(x, w, d / a)
        return x1 + (1 - a) * (x - x1)

    def generator():
        for z in watermarked:
            z0 = f(z, 0, delta, alpha)
            z1 = f(z, 1, delta, alpha)
            d0 = np.abs(z - z0)
            d1 = np.abs(z - z1)
            if d0 < d1:
                yield 0
            else:
                yield 1
    return generator()
