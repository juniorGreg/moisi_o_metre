from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitmap

sitemaps = {
    "posts": PostSitmap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.index, name="post"),
    path('about/', views.about, name="about"),
    path('references/', views.references, name="references"),
    path('contact/', views.contact, name="contact"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('posts/<int:id>', views.posts, name="posts_with_id"),
    path('posts', views.posts, name="posts"),
    path('tests', views.tests, name="tests")
]
