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
    tasks.imageupload.delay(pid)

    return HttpResponse(json.dumps({"status": "success"}))


@csrf_exempt
def product_info_details(request):
    pid = request.POST.get("pid")
    name = request.POST.get("name")
    price = request.POST.get("price")

    product = Product.objects.get(id=pid)
    product.name = name
    product.price = price
    product.save()

    return HttpResponse(json.dumps({"status": "success"}))


# product fetch API
@csrf_exempt
def fetch_product_details(request):
    products = Product.objects.all()

    data = []
    for product in products:
        pdata = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': json.loads(product.image),
            'image256': json.loads(product.image256),
            'image512': json.loads(product.image512)
        }
        data.append(pdata)

    data = json.dumps({'products': data})
    return HttpResponse(data)
