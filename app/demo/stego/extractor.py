from app.demo.stego.utils import switch
from app.demo.stego.embedder import Template, algorithm_switcher


class Extractor(Template):

    def __init__(self, **kwargs):
        super(Extractor, self).__init__(**kwargs)

    def __call__(self, image, cb=None):
        try:
            function = switch(algorithm_switcher, self.algorithm)[2]
            return function(image, None, cb, **self.settings)
        except IndexError:
            raise Exception(f'Extract function for {self.algorithm} algorithm may not available')
