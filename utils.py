import PIL
from PIL import Image


def resize_image(image_path, dimensions):
    img = Image.open(image_path)
    return img.thumbnail(dimensions)
