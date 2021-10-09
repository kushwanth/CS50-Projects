from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("myorders", views.myorders, name="myorders"),
    path("checkout", views.checkout, name="checkout")
]
