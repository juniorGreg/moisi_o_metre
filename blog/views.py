from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .models import *
from .forms import CommentForm

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer

vuejs = "https://cdn.jsdelivr.net/npm/vue@2.6.11/dist/vue.min.js"

if settings.DEBUG:
    vuejs = "https://cdn.jsdelivr.net/npm/vue/dist/vue.js"



# Create your views here.
def index(request, id=-1):

    post_ids = list(Post.objects.order_by('-date_created').values_list('id', flat=True))
    if id in post_ids:

        index = post_ids.index(id)
        if index > 0 :
            del post_ids[index]
            post_ids.insert(0, id)    

    context = {"post_ids": post_ids, 'vuejs' : vuejs}
    return render(request, "blog/index.html", context)

def about(request):
    about = About.objects.all()[0]
    context = {'about': about, 'vuejs': vuejs}
    return render(request, "blog/about.html", context)

def references(request):
    references = Reference.objects.filter(is_global=True)
    context = {'references': references, "vuejs": vuejs}
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

    context = {'vuejs': vuejs}

    return render(request, "blog/contact.html", context)


#API
@api_view(['GET'])
def posts(request, id=-1):
    if id == -1:
        post = Post.objects.order_by('-date_created')[0]
    else:
        post = Post.objects.get(id=id)

    serializer = PostSerializer(post)
    return Response(serializer.data)
