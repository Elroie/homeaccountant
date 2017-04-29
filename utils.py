import PIL
from PIL import Image

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def resize_image(image_path, dimensions):
    img = Image.open(image_path)
    return img.thumbnail(dimensions)
