from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="bullshit_index"),
    path("website/", views.website, name="website")
]
