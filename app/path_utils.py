import os
from flask import url_for


def get_url(path, file, default):
    """
    Get url for a file if exists else url for other default file
    :param path: absolute path for files
    :param file: any filename
    :param default: any filename for existing file
    :return: url_for
    """
    new_path = os.path.join(path, file)
    fn = os.path.basename(path)
    if os.path.isfile(new_path):
        fn += f'/{file}'
    else:
        fn += f'/{default}'
    return url_for('static', filename=fn)
