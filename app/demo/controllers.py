import os
import numpy as np
from PIL import Image
import cv2
from flask import render_template, request, current_app, redirect, url_for, make_response, jsonify

from . import mod_demo, MOD_NAME
from .stego.embedder import Embedder
from .stego.extractor import Extractor
from .stego.modifier import Modifier
from .stego.utils import str_to_binary
from app.path_utils import get_url


@mod_demo.errorhandler(500)
def server_exception(e):
    return jsonify(error=str(e)), 500


@mod_demo.route('', methods=['GET'])
def get_demo():
    try:
        # image (1st img)
        image_url = get_url(
            current_app.config['IMAGE_DIR'],
            current_app.config['IMAGE_FN'],
            current_app.config['DEFAULT_FN']
        )
        # embed (2nd img)
        embed_url = get_url(
            current_app.config['EMBED_DIR'],
            current_app.config['EMBED_FN'],
            current_app.config['DEFAULT_FN']
        )
        # modified (3rd img)
        mod_url = get_url(
            current_app.config['MOD_DIR'],
            current_app.config['MOD_FN'],
            current_app.config['DEFAULT_FN']
        )

        settings = Embedder.available_settings()
        settings.update(Modifier.available_settings())
        return render_template(
            f'{MOD_NAME}/demo.html',
            image=image_url,
            embed=embed_url,
            mod=mod_url,
            settings=settings
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )


@mod_demo.route('uploader/image', methods=['POST'])
def upload_image():
    try:
        f = request.files['upload-image'].read()
        if f:
            np_img = np.fromstring(f, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img.astype('uint8'))
            img.save(
                os.path.join(current_app.config['IMAGE_DIR'], current_app.config['IMAGE_FN']),
                'PNG'
            )
        return make_response(
            jsonify({'msg': 'Image uploaded successfully'}),
            200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )


@mod_demo.route('uploader/mod', methods=['POST'])
def upload_mod():
    try:
        f = request.files['upload-mod'].read()
        if f:
            np_img = np.fromstring(f, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img.astype('uint8'))
            img.save(
                os.path.join(current_app.config['MOD_DIR'], current_app.config['MOD_FN']),
                'PNG'
            )
        return make_response(
            jsonify({'msg': 'Modified image uploaded successfully'}),
            200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )


@mod_demo.route('embedding', methods=['POST'])
def embed_watermark():
    # try:
        settings = request.form.to_dict()
        img = Image.open(os.path.join(current_app.config['IMAGE_DIR'], current_app.config['IMAGE_FN']))
        watermark = str_to_binary(settings['watermark'])
        cb = current_app.config['progress_cb']

        cb.add_max_value(1)
        embedder = Embedder(**settings)
        new_img = embedder(img, watermark, cb=cb)
        new_img.save(
            os.path.join(current_app.config['EMBED_DIR'], current_app.config['EMBED_FN']),
            'PNG'
        )
        cb.add_current_value(1)
        return make_response(
            jsonify({'msg': 'Watermark embedded successfully'}),
            200
        )
    # except Exception as e:
    #     return make_response(
    #         jsonify({'msg': str(e)}),
    #         500
    #     )


@mod_demo.route('modify', methods=['POST'])
def modify_image():
    try:
        settings = request.form.to_dict()
        img = Image.open(os.path.join(current_app.config['EMBED_DIR'], current_app.config['EMBED_FN']))
        cb = current_app.config['progress_cb']

        cb.add_max_value(1)
        new_img = Modifier(**settings)(img)
        new_img.save(
            os.path.join(current_app.config['MOD_DIR'], current_app.config['MOD_FN']),
            'PNG'
        )
        cb.add_current_value(1)

        return make_response(
            jsonify({'msg': 'Image modified successfully'}),
            200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )


@mod_demo.route('extract', methods=['POST'])
def extract_watermark():
    try:
        settings = request.form.to_dict()
        img = Image.open(os.path.join(current_app.config['MOD_DIR'], current_app.config['MOD_FN']))
        cb = current_app.config['progress_cb']

        cb.add_max_value(1)
        extracted = Extractor(**settings)(img, cb=cb)
        cb.add_current_value(1)

        return make_response(
            jsonify({
                'msg': 'Watermark extracted successfully',
                'watermark': extracted
            }),
            200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )
