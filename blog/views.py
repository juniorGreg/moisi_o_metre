from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .models import *
from .forms import CommentForm

# Create your views here.
def index(request):
    posts = Post.objects.all()
    print(posts)
    context = {"posts": posts}
    return render(request, "blog/index.html", context)

def about(request):
    about = About.objects.all()[0]
    context = {'about': about}
    return render(request, "blog/about.html", context)

def references(request):
    references = Reference.objects.all()
    context = {'references': references}
    return render(request,"blog/references.html", context)

def contact(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                settings.DEFAULT_FROM_EMAIL,
                ['junior.gregoire@gmail.com']
            )
            return redirect('index')

    return render(request, "blog/contact.html")
