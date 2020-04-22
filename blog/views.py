from django.shortcuts import render, redirect
from .models import *
from .forms import CommentForm

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/index.html", context)

def about(request):
    return render(request, "blog/about.html")

def references(request):
    return render(request,"blog/references.html")

def contact(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect('index')

    return render(request, "blog/contact.html")
