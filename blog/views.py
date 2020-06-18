from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.templatetags.static import static

from .models import *
from django.contrib.sites.models import Site
from .forms import CommentForm

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer



def get_main_context(tag_title, tag_desc, tag_url, tag_image="/images/moisiometre.png"):
    if "http" not in tag_image:
        tag_image = static(tag_image)

    tag = {
        'title': tag_title,
        'description': tag_desc,
        'image': tag_image,
        'url': 'https://%s%s' % (Site.objects.get_current().domain, tag_url)
    }

    context = {'tag': tag}

    if settings.DEBUG:
        context['vuejs'] = "https://cdn.jsdelivr.net/npm/vue/dist/vue.js"
    else:
        context['vuejs'] = "https://cdn.jsdelivr.net/npm/vue@2.6.11/dist/vue.min.js"

    return context




# Create your views here.
def index(request, id=-1):

    post_ids = list(Post.objects.order_by('-date_created').values_list('id', flat=True))
    if id in post_ids:

        index = post_ids.index(id)
        if index > 0 :
            del post_ids[index]
            post_ids.insert(0, id)

    post = Post.objects.get(id=post_ids[0])

    if post.image:
        context = get_main_context(post.title[0:70], post.content[:200], post.get_absolute_url(),  post.image.url)
    else:
        context = get_main_context(post.title[0:70], post.content[:200], post.get_absolute_url())

    context["post_ids"] = post_ids

    return render(request, "blog/index.html", context)

def about(request):
    about = About.objects.all()[0]

    context = get_main_context("À propos", about.text[:200] , "/about")

    context['about'] = about
    return render(request, "blog/about.html", context)

def references(request):
    references = Reference.objects.filter(is_global=True)
    context = get_main_context("Les références", "Voici mes références." , "/references")
    context['references'] = references
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

    context = get_main_context("Contact", "Si vous voulez me contacter. C'est ici!" , "/contact")

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
