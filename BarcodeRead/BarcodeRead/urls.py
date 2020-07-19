
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.it_works),
    path('admin/', admin.site.urls),
    path('read_barcode/', views.read_barcode),
    path('api/v1/get_barcode/', views.get_barcode, name='get_barcode')
]
