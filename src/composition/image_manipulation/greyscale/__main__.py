from os import environ
import uuid

import requests
from io import BytesIO
from base64 import b64encode, b64decode

import binascii
from PIL import Image, UnidentifiedImageError, ImageOps
from redis import Redis


V_DEFAULT_RESIZE_RATIO: float = 10.0
DEFAULT_IMAGE_URL: str = "https://www.nasa.gov/sites/default/files/images/440676main_STScI-2007-04a-full_full.jpg"
DEFAULT_REDIS_KEY: str = str(uuid.uuid1())
REDIS_HOST: str = environ.get("OWDEV_REDIS_SERVICE_HOST")
REDIS_PORT: str = environ.get("OWDEV_REDIS_SERVICE_PORT")
REDIS_DB: int = 7


def get_image(in_type: str, location: object) -> Image:
    image = None

    if in_type == 'url':
        data = requests.get(str(location)).content
        image = Image.open(BytesIO(data))
    elif in_type == 'local':
        image = Image.open(str(location))
    elif in_type == 'redis':
        # get raw data see@ https://github.com/andymccurdy/redis-py/issues/658
        redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        data = redis.get(str(location))
        image = Image.open(BytesIO(b64decode(data)))

    return image


def store_image(out_type: str, location: object, image: Image):
    if out_type == 'url':
        pass
    elif out_type == 'local':
        image.save(str(location))
    elif out_type == 'redis':
        redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        data = BytesIO()
        image.save(data, format='JPEG')
        redis.set(location, b64encode(data.getvalue()))
        data.close()


def remove_image(in_type: str, location: object):
    if in_type == 'url':
        pass
    elif in_type == 'local':
        pass
    elif in_type == 'redis':
        redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        redis.delete(str(location))


def resize(image: Image, resize_ratio: float) -> Image:
    print(f"Image size before processing: {{ image.size: {image.size} }}")
    x_resized = image.size[0] - int(image.size[0] * resize_ratio / 100)
    y_resized = image.size[1] - int(image.size[1] * resize_ratio / 100)
    image_resized = image.resize((x_resized, y_resized))
    print(f"Image resized: {{ image.size: {image_resized.size} }}")
    return image_resized


def greyscale(image: Image) -> Image:
    return ImageOps.grayscale(image)


def main(params: dict) -> dict:
    try:
        result: bool = str(params["result"]) in ['True', 'true', 1]
    except KeyError:
        result: bool = False
    try:
        in_type: str = str(params["in_type"])
        in_location: str = str(params["in_location"])
    except KeyError:
        in_type: str = "url"
        in_location: str = DEFAULT_IMAGE_URL
    try:
        out_type: str = str(params["out_type"])
        out_location: str = str(params["out_location"])
    except KeyError:
        out_type: str = "redis"
        out_location: str = environ["__OW_ACTIVATION_ID"]

    try:
        image: Image = get_image(in_type, in_location)
        remove_image(in_type, in_location)
        new_image = greyscale(image)
        # store_image(out_type, out_location, new_image)
    except (NameError, binascii.Error, FileNotFoundError, UnidentifiedImageError, ValueError, TypeError):
        return {
            "error": "Error processing image."
        }

    response: dict = {
        "in_type": "redis",
        "in_location": in_location,
        "out_type": "redis",
        "out_location": out_location,
    }
    if params.get("$scheduler") is not None:
        response["$scheduler"] = params["$scheduler"] 
    if result:
        data = BytesIO()
        new_image.save(data, format='JPEG')
        response["image"] = b64encode(data.getvalue())
    return response


# if __name__ == '__main__':
#     main({
#         "in_type": "url",
#         # "in_location": "https://www.nasa.gov/sites/default/files/thumbnails/image/5091372229_ebca868ffd_o.jpeg",
#         "out_type": "local",
#         "out_location": "/Volumes/Ramdisk/img.jpg"
#     })
