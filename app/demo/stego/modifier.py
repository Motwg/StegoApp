import os
from PIL import ImageEnhance, Image
from flask import current_app

from app.demo.stego.utils import switch


def attack_switcher():
    # case/key: (name, attack, *optional args)
    return {
        'crop_20': ('Crop 20%', crop_20),
        'crop_50': ('Crop 50%', crop_50),
        'sharpen': ('Sharpen', sharpen),
        'blur': ('Blur', blur),
        'conv_bmp_24b': ('BMP 24-bit conversion', conv_bmp_24b),
        'conv_bmp_256c': ('BMP 256-colours conversion', conv_bmp_no_col, (256,)),
        'conv_bmp_64c': ('BMP 64-colours conversion', conv_bmp_no_col, (64,)),
        'conv_bmp_16c': ('BMP 16-colours conversion', conv_bmp_no_col, (16,)),
        'conv_png': ('PNG conversion', lambda img: img),
        'conv_tiff': ('TIFF conversion', conv_tiff),
        'conv_jp2': ('JPEG 2000 conversion', conv_jp2),
        'jpeg_10': ('JPEG compression 10%', compression, (90,)),
        'jpeg_20': ('JPEG compression 20%', compression, (80,)),
        'jpeg_50': ('JPEG compression 50%', compression, (50,))
    }, 'crop_20'


def crop_20(img):
    assert isinstance(img, Image.Image)
    width, height = img.size
    return img.crop((width // 10, height // 10, width * 9 // 10, height * 9 // 10))


def crop_50(img):
    assert isinstance(img, Image.Image)
    width, height = img.size
    return img.crop((width // 4, height // 4, width * 3 // 4, height * 3 // 4))


def sharpen(img):
    assert isinstance(img, Image.Image)
    return ImageEnhance.Sharpness(img).enhance(2)


def blur(img):
    assert isinstance(img, Image.Image)
    return ImageEnhance.Sharpness(img).enhance(0.5)


def conv_tiff(img):
    assert isinstance(img, Image.Image)
    img.save(
        os.path.join(current_app.config['MOD_DIR'], 'img.tiff'),
        'TIFF'
    )
    tiff = Image.open(os.path.join(current_app.config['MOD_DIR'], 'img.tiff'))
    tiff.save(
        os.path.join(current_app.config['MOD_DIR'], 'from_tiff.png'),
        'PNG'
    )
    return Image.open(os.path.join(current_app.config['MOD_DIR'], 'from_tiff.png'))


def conv_jp2(img):
    assert isinstance(img, Image.Image)
    img.save(
        os.path.join(current_app.config['MOD_DIR'], 'img.jp2'),
        'JPEG2000'
    )
    tiff = Image.open(os.path.join(current_app.config['MOD_DIR'], 'img.jp2'))
    tiff.save(
        os.path.join(current_app.config['MOD_DIR'], 'from_jp2.png'),
        'PNG'
    )
    return Image.open(os.path.join(current_app.config['MOD_DIR'], 'from_jp2.png'))


def conv_bmp_24b(img):
    assert isinstance(img, Image.Image)
    img.save(
        os.path.join(current_app.config['MOD_DIR'], 'img.bmp'),
        'BMP'
    )
    bmp = Image.open(os.path.join(current_app.config['MOD_DIR'], 'img.bmp'))
    bmp.save(
        os.path.join(current_app.config['MOD_DIR'], 'from_bmp.png'),
        'PNG'
    )
    return Image.open(os.path.join(current_app.config['MOD_DIR'], 'from_bmp.png'))


def conv_bmp_no_col(img, no_colours):
    assert isinstance(img, Image.Image)
    bmp = img.convert('P', palette=Image.ADAPTIVE, colors=no_colours)
    return bmp.convert('RGB')


def compression(img, quality):
    assert isinstance(img, Image.Image)
    img.save(
        os.path.join(current_app.config['MOD_DIR'], 'img.jpg'),
        'JPEG',
        quality=quality,
        subsampling=0
    )
    jpeg = Image.open(os.path.join(current_app.config['MOD_DIR'], 'img.jpg'))
    jpeg.save(
        os.path.join(current_app.config['MOD_DIR'], 'from_jpg.png'),
        'PNG'
    )
    return Image.open(os.path.join(current_app.config['MOD_DIR'], 'from_jpg.png'))


class Modifier:

    def __init__(self, **kwargs):
        self.attack = kwargs.get('modification', 'crop_20')

    def __call__(self, img, cb=None):
        function = switch(attack_switcher, self.attack)[1]
        try:
            args = switch(attack_switcher, self.attack)[2]
            return function(img, *args)
        except IndexError:
            return function(img)

    @staticmethod
    def available_settings():
        # get all possible options from switchers
        settings = {
            name.replace('_switcher', ''): func()[0] for name, func in tuple(globals().items())
            if name.endswith('_switcher')
        }
        # filter out unimportant information (leaves only names)
        return {setting_name: {k: v[0] for k, v in d.items()} for setting_name, d in settings.items()}
