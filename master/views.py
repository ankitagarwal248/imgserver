import json
from master.models import *
from django.http import HttpResponse
from django.shortcuts import render
import StringIO
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import redis
from . import tasks


def product_info(request):
    return render(request, 'master/productinfo.html', {})


@csrf_exempt
def product_info_image(request):

    pid = request.POST.get("pid")
    img_file = request.FILES['img']

    output = StringIO.StringIO()
    im = Image.open(img_file)
    im.save(output, format=im.format)

    # storing image in redis
    redis_img_id = 'image:'+pid
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(redis_img_id, output.getvalue())
    output.close()

    # asynchronously (using celery) resizing uploaded image and storing it in db
    tasks.imageupload256.delay(pid)
    tasks.imageupload512.delay(pid)

    return HttpResponse(json.dumps({"status": "success"}))


@csrf_exempt
def product_info_details(request):
    pid = request.POST.get("pid")
    name = request.POST.get("name")
    price = request.POST.get("price")

    # store product details in db

    return HttpResponse(json.dumps({"status": "success"}))


@csrf_exempt
def fetch_product_details(request):
    pid = request.GET.get("pid")
    product = Product.objects.get(id=pid)

    data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': product.image,
        'image256': product.image256,
        'image512': product.image512
    }

    data = json.dumps(data)
    return HttpResponse(data)
