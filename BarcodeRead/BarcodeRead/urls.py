
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.it_works),
    path('admin/', admin.site.urls),
    path('read_barcode/', views.read_barcode)
]
