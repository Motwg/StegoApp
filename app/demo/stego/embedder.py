import app.demo.stego.algorithms as alg
from app.demo.stego.utils import switch


def channel_switcher():
    # case/key: (name, chosen channels)
    return {
        'r': ('Red', [0]),
        'g': ('Green', [1]),
        'b': ('Blue', [2]),
        'all': ('RGB - same watermark on every channel', [0, 1, 2])
    }, 'b'  # default set blue


def algorithm_switcher():
    # case/key: (name, algorithm, optional - invert algorithm)
    return {
        'lsb': ('Least Significant Bit', alg.lsb, alg.i_lsb),
        'qim': ('QIM', alg.qim, alg.i_qim),
        'dc_qim': ('DC-QIM', alg.dc_qim, alg.i_dc_qim),
        'none': ('None', lambda x, *args, **kwargs: x)
    }, 'lsb'  # default set lsb


class Template:
    def __init__(self, **kwargs):
        self.algorithm = kwargs.get('algorithm', 'lsb')
        self.settings = {
            'no_channels': 3,
            'channel': switch(channel_switcher, kwargs.get('channel'))[1],
            'delta': int(kwargs.get('delta', 1)),
            'alpha': float(kwargs.get('alpha', 0.95))
        }

    @staticmethod
    def available_settings():
        # get all possible options from switchers
        settings = {
            name.replace('_switcher', ''): func()[0] for name, func in tuple(globals().items())
            if name.endswith('_switcher')
        }
        # filter out unimportant information
        return {setting_name: {k: v[0] for k, v in d.items()} for setting_name, d in settings.items()}


class Embedder(Template):

    def __init__(self, **kwargs):
        super(Embedder, self).__init__(**kwargs)

    def __call__(self, image, watermark, cb=None):
        function = switch(algorithm_switcher, self.algorithm)[1]
        return function(image, watermark, cb, **self.settings)


if __name__ == '__main__':
    Embedder.available_settings()
