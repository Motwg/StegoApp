# Define the application directory
import os

# Statement for enabling the development environment
DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'app/static/images')
EMBED_DIR = os.path.join(BASE_DIR, 'app/static/embeds')
MOD_DIR = os.path.join(BASE_DIR, 'app/static/modified')

DEFAULT_FN = 'default_image.png'
IMAGE_FN = 'image.png'
EMBED_FN = 'embed_image.png'
MOD_FN = 'modified_image.png'

# THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "s3cr3t"

# Secret key for signing cookies
SECRET_KEY = "s3cr3t"
