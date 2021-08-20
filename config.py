import os

# Statement for enabling the development environment
DEBUG = False


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# stego module
IMAGE_DIR = os.path.join(BASE_DIR, 'app/static/images')
EMBED_DIR = os.path.join(BASE_DIR, 'app/static/embeds')
MOD_DIR = os.path.join(BASE_DIR, 'app/static/modified')
MODEL_DIR = os.path.join(BASE_DIR, 'app/models')

DEFAULT_FN = 'default_image.png'

# THREADS_PER_PAGE = 2

# Tensorflow logging variable {'0', '1', '2', '3'}
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "s3cr3t"

# Secret key for signing cookies
SECRET_KEY = "s3cr3t"
