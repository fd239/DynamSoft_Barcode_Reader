
from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/get_barcode/', views.get_barcode, name='get_barcode')
]
