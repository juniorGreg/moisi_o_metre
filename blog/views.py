from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.templatetags.static import static
from django.http import Http404
from django.db.models import Q

from .models import *
from django.contrib.sites.models import Site
from .forms import CommentForm

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, SearchedPostSerializer

import requests


# Create your views here.
def index(request, id=-1):
    if request.user.is_authenticated:
        post_ids = list(Post.objects.order_by('-date_created').values_list('id', flat=True))
    else:
        post_ids = list(Post.objects.filter(admin_only=False).order_by('-date_created').values_list('id', flat=True))


    if id in post_ids:

        index = post_ids.index(id)
        if index > 0 :
            del post_ids[index]
            post_ids.insert(0, id)

    post = Post.objects.get(id=post_ids[0])

    def get_post_description(post):
        content = post.content
        if len(content) == 0:
            content = post.rottenpoint_set.order_by("order")[0].description
        return content

    post_description = get_post_description(post)

    context = {}
    context["post_ids"] = post_ids
    context["post"] = post
    context["post_description"] = post_description
    next_post_noscript = list(filter(lambda post_id: post_id < post.id, post_ids))
    if next_post_noscript:
        context["next_post_noscript"] = next_post_noscript[0]
    return render(request, "blog/index.html", context)

def support(request):
    return render(request, "blog/support.html")

def tests(request):
    if not settings.DEBUG:
        raise Http404

    return render(request, "blog/tests.html")

def about(request):
    about = About.objects.all()[0]

    context = {}

    context['about'] = about
    return render(request, "blog/about.html", context)

def references(request):
    references = Reference.objects.filter(is_global=True)
    context = {}
    context['references'] = references
    return render(request,"blog/references.html", context)

def contact(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)

            def get_message():
                base_message = form.cleaned_data["message"]
                email = form.cleaned_data["email"]

                if email:
                    new_message = "{base}\n\nEmail pour répondre: {email}".format(base=base_message, email=email)
                    return new_message

                else:
                    return base_message

            message = get_message()
            #print(message)

            send_mail(
                form.cleaned_data['subject'],
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_ADMIN]
            )
            return redirect('index')

    context = {}

    return render(request, "blog/contact.html", context)

def bullshit_o_metre(request):
    return render(request, "blog/bullshit_o_metre.html")

def quiz(request):
    return render(request, "blog/quiz.html")





#API
@api_view(['GET'])
def posts(request, id=-1):
    if id == -1:
        post = Post.objects.prefetch_related('rottenpoint_set').prefetch_related("sources").select_related("statistics").select_related("media_link").order_by('-date_created').first()
    else:
        post = Post.objects.prefetch_related('rottenpoint_set').prefetch_related("sources").select_related("statistics").select_related("media_link").get(id=id)

    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
def search(request, word):
    if request.user.is_authenticated:
        posts = Post.objects.filter(Q(content__icontains=word) | Q(title__icontains=word) )
    else:
        posts = Post.objects.filter(admin_only=False).filter(Q(content__icontains=word) | Q(title__icontains=word))
    serializer = SearchedPostSerializer(posts[:5], many=True)
    return Response(serializer.data)

@api_view(["GET"])
def location(request):
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
    print(ip_address)
    if ip_address == '127.0.0.1' or ip_address == '192.168.1.1':
        ip_address =  "173.176.163.196"

    if ',' in ip_address:
        ip_address = ip_address.split(',')[0]

    req_location = requests.get("https://freegeoip.app/json/%s" % ip_address)
    if req_location.status_code == 200:
        return Response(req_location.json())
    else:
        return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
