import cv2
import numpy as np
import os
from flask import render_template, request, current_app, redirect, url_for, make_response, jsonify, abort
from PIL import Image

from . import mod_demo, MOD_NAME
from .stego.embedder import Embedder
from .stego.extractor import Extractor
from .stego.modifier import Modifier
from .stego.server_model import ServerModel
from .stego.utils import str_to_binary, encode_img, decode_img


@mod_demo.errorhandler(500)
def server_exception(e):
    return jsonify(error=str(e)), 500


@mod_demo.route('', methods=['GET'])
def get_demo():
    try:
        # image (1st img)
        image_url = encode_img(Image.open(
            os.path.join(current_app.config['IMAGE_DIR'], current_app.config['DEFAULT_FN'])
        ))
        # embed (2nd img)
        embed_url = encode_img(Image.open(
            os.path.join(current_app.config['EMBED_DIR'], current_app.config['DEFAULT_FN'])
        ))
        # modified (3rd img)
        mod_url = encode_img(Image.open(
            os.path.join(current_app.config['MOD_DIR'], current_app.config['DEFAULT_FN']))
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
        abort(500)


@mod_demo.route('uploader/image', methods=['POST'])
def upload_image():
    try:
        f = request.files['upload-image'].read()
        np_img = np.fromstring(f, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'))
        enc_img = encode_img(img)
        return make_response(
            jsonify({
                'msg': 'Image uploaded successfully',
                'img': enc_img
            }), 200
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
        np_img = np.fromstring(f, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'))
        enc_img = encode_img(img)
        return make_response(
            jsonify({
                'msg': 'Modified image uploaded successfully',
                'img': enc_img
            }), 200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )


@mod_demo.route('embedding', methods=['POST'])
def embed_watermark():
    try:
        settings = request.form.to_dict()
        img = decode_img(settings.pop('up_img'))
        watermark = str_to_binary(settings['watermark'])
        cb = current_app.config['progress_cb']

        cb.add_max_value(1)
        embedder = Embedder(**settings)
        new_img = embedder(img, watermark, cb=cb)
        enc_img = encode_img(new_img)
        cb.add_current_value(1)

        return make_response(
            jsonify({
                'msg': 'Watermark embedded successfully',
                'img': enc_img
            }), 200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )


@mod_demo.route('modify', methods=['POST'])
def modify_image():
    try:
        settings = request.form.to_dict()
        img =  decode_img(settings.pop('emb_img'))
        cb = current_app.config['progress_cb']

        cb.add_max_value(1)
        new_img = Modifier(**settings)(img)
        enc_img = encode_img(new_img)
        cb.add_current_value(1)

        return make_response(
            jsonify({
                'msg': 'Image modified successfully',
                'img': enc_img
            }), 200
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
        img = decode_img(settings.pop('mod_img'))
        cb = current_app.config['progress_cb']

        cb.add_max_value(1)
        extracted = Extractor(**settings)(img, cb=cb)
        cb.add_current_value(1)

        return make_response(
            jsonify({
                'msg': 'Watermark extracted successfully',
                'watermark': extracted
            }), 200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )


@mod_demo.route('steganalysis', methods=['POST'])
def steganalysis():
    try:
        settings = request.form.to_dict()
        img = decode_img(settings.pop('emb_img'))
        cb = current_app.config['progress_cb']
        assert isinstance(img, Image.Image)
        cb.add_max_value(1)
        x = ServerModel()(img)
        cb.add_current_value(1)
        return make_response(
            jsonify({
                'msg': 'Steganalysis completed',
                'r': f'{x[0][0]}',
                'g': f'{x[1][0]}',
                'b': f'{x[2][0]}',
                'r_p': f'{x[0][1]}',
                'g_p': f'{x[1][1]}',
                'b_p': f'{x[2][1]}'
            }), 200
        )
    except Exception as e:
        return make_response(
            jsonify({'msg': str(e)}),
            500
        )
