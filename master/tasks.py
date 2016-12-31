import PIL
import time
from celery import shared_task
import StringIO
from PIL import Image
import redis
from master.models import *
import json


@shared_task
def imageupload(pid):
    img = get_redis_image(pid)
    img_width, img_height = img.size
    size = str(img_width) + 'x' + str(img_height)

    print size

    img256 = img.resize((256, 256), PIL.Image.ANTIALIAS)
    img512 = img.resize((512, 512), PIL.Image.ANTIALIAS)

    # save images on aws bucket

    image_data = {'url': 'http://aws.com/dsd', 'size': size}
    image256_data = {'url': 'http://aws.com/dsd', 'size': '256x256'}
    image512_data = {'url': 'http://aws.com/dsd', 'size': '512x512'}

    # product = Product.objects.get(id=pid)
    # product.image = json.dumps(image_data)
    # product.image256 = json.dumps(image256_data)
    # product.image512 = json.dumps(image512_data)
    # product.save()

    img.save('some256.png')
    return True


def get_redis_image(pid):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_img_id = 'image:' + pid
    ri = r.get(redis_img_id)
    stream = StringIO.StringIO(ri)
    img = Image.open(stream)
    return img


def delete_redis_images():
    pass


def bgtasks(pid):
    delete_redis_images()


@shared_task
def dummy_task(x, y):
    print 'dummy tasks begins'
    time.sleep(5)
    return "The sum is: " + str(x + y)


@shared_task
def dummy_data(x, y):
    print 'dummy data task begins'
    time.sleep(5)
    return "The multiple is: " + str(x*y)


