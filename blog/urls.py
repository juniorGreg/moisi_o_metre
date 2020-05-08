from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.index, name="post"),
    path('about/', views.about, name="about"),
    path('references/', views.references, name="references"),
    path('contact/', views.contact, name="contact")
]
