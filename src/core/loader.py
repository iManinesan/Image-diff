"""Loader module contains functions for loading and saving images.
"""
from os.path import splitext
from wand.image import Image
import requests
from scipy import misc

import utils

def load_image_from_file(file):
    return Image.(filename=file)


def load_image_from_url(url):
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise ValueError('Invalid image URL')

    return load_image_from_file(response.raw)


def save_image(image, path):
    filename, extension = splitext(path)
    image.save(filename=path)
