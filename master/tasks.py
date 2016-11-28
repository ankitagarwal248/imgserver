import PIL
from celery import shared_task,current_task
import StringIO
from PIL import Image
import redis


@shared_task
def imageupload256(pid):
    img = get_redis_image(pid)
    img = img.resize((256, 256), PIL.Image.ANTIALIAS)
    img.save('some256.png')
    return True


@shared_task
def imageupload512(pid):
    img = get_redis_image(pid)
    img = img.resize((512, 512), PIL.Image.ANTIALIAS)
    img.save('some512.png')
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
