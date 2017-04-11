import PIL
from PIL import Image


def singleton(class_):
    '''A singleton pattern as a decorator'''
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


def resize_image(image_path, dimensions):
    img = Image.open(image_path)
    return img.thumbnail(dimensions)
