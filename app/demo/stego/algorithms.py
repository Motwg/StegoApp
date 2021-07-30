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


@wr.generate
def double_qim(pixels, d_watermark, *args, **kwargs):
    delta = 4

    def q(x, w):
        return np.round(x / delta) * delta - (-1) ** w * delta / 4

    def q1(x, w):
        return np.round(x / delta) * delta - (-1) ** w * delta / 2

    def generator():
        for x, w in zip(pixels, d_watermark):
            yield q(q1(x, w % 2), w // 2)

    return generator()


@wr.i_algorithm_wrapper
@wr.generate
def show_watermark(pixels, watermark, *args, **kwargs):
    def generator():
        for x, y in zip(pixels, watermark):
            if y == 0:
                yield 0
            elif y == 1:
                yield 1
            else:
                raise Exception('Wrong watermark')

    return generator()


# @wr.generate
# def dm_qim(pixels, wm, *args):
#     np.random.seed(0)
#     delta = 2
#     delta2 = delta / 2
#     d0 = np.random.uniform(-delta2, delta2)
#     if d0 < 0:
#         d1 = d0 + delta2
#     else:
#         d1 = d0 - delta2
#     d = (d0, d1)
#
#     def q(x):
#         return np.round(x / delta) * delta
#
#     def generator():
#         for x, m in zip(pixels, wm):
#             yield q(x + d[int(m)]) - d[int(m)]
#
#     return generator()


# @wr.generate
# def i_dm_qim(pixels, *args):
#     np.random.seed(0)
#     delta = 0.5
#     delta2 = delta / 2
#     d0 = np.random.uniform(-delta2, delta2)
#     if d0 < 0:
#         d1 = d0 + delta2
#     else:
#         d1 = d0 - delta2
#     d = (d0, d1)
#
#     def q(x):
#         return np.round(x / delta) * delta
#
#     def generator():
#         for z in pixels:
#             z0 = abs(z - q(z + d[0]) + d[0])
#             z1 = abs(z - q(z + d[1]) + d[1])
#             yield 0 if z0 < z1 else 1
#
#     return generator()


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
                yield 255
    return generator()


if __name__ == '__main__':
    values = [x for x in range(256)]

    for i in range(2, 12):
        print(f'delta: {i}')
        kw = {
            'delta': i,
            'alpha': 0.65
        }
        resp1 = dc_qim([values, values, values], [0] * 256, **kw)
        resp2 = dc_qim([values, values, values], [1] * 256, **kw)
        # resp3 = qim([values, values, values], [0] * 256)
        # resp4 = qim([values, values, values], [1] * 256)
        print([resp1[2][y] for y in range(256)])
        print([resp2[2][y] for y in range(256)])
        # print([resp3[2][y] for y in range(256)])
        # print([resp4[2][y] for y in range(256)])
        resp3 = list(i_dc_qim(resp1, **kw)[2])  # lsb([values, values, values], [0] * 256)
        resp4 = list(i_dc_qim(resp2, **kw)[2])  # lsb([values, values, values], [1] * 256)
        print(resp3)
        print(resp4)
