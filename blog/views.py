from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    posts = Post.objects.all()
    print(posts)
    context = {"posts": posts}
    return render(request, "blog/index.html", context)
