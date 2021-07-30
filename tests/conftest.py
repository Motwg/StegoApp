import os
import pytest
from PIL import Image

from app import create_app


TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def image():
    return Image.open(os.path.join(TEST_DIR, 'img0.png'))


@pytest.fixture
def b_watermark():
    return [0, 1, 0, 0, 1]
