import json

from django.http import HttpResponse
from django.shortcuts import render
import StringIO
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import redis
from .tasks import imageupload256, imageupload512


def product_info(request):
    return render(request, 'master/productinfo.html', {})


@csrf_exempt
def product_info_image(request):

    pid = request.POST.get("pid")
    img_file = request.FILES['img']

    print pid, "5555555555"

    output = StringIO.StringIO()
    im = Image.open(img_file)
    im.save(output, format=im.format)

    redis_img_id = 'image:'+pid
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(redis_img_id, output.getvalue())
    output.close()

    return HttpResponse(json.dumps({"status": "success"}))


@csrf_exempt
def product_info_details(request):
    pid = request.POST.get("pid")
    name = request.POST.get("name")
    price = request.POST.get("price")

    job = imageupload256.delay(pid)
    job = imageupload512.delay(pid)

    return HttpResponse(json.dumps({"status": "success"}))
