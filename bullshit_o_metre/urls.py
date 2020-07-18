from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="bullshit_index"),
    path("evaluate_tainted_lemmas", views.evaluate_tainted_lemmas, name="evaluate_tainted_lemmas"),
    path("website/", views.website, name="website")
]
