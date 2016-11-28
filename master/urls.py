from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^product_info/$', views.product_info),
    url(r'^product_info_image/$', views.product_info_image),
    url(r'^product_info_details/$', views.product_info_details),
    url(r'^fetch_product_details/$', views.fetch_product_details),
]
