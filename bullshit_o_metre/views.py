from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

from django.forms import modelformset_factory
from .bullshit_detector_api import evaluate_website, add_website


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


# Create your views here.
@login_required(login_url="index")
def index(request):

    labeled_website_count = LabeledWebSite.objects.count()

    context = {"labeled_website_count": labeled_website_count}

    return render(request, "bullshit_o_metre/index.html", context)



@api_view(['GET', 'POST'])
def website(request):

    if request.method == "GET":
        url = request.GET.get('url')

        if "http" not in url:
            return Response({'error': 'url not valid', 'error_no': '1'})

        print(url)

        title, score = evaluate_website(url)


        return Response({'title': title, 'score': score})

    if request.method == "POST" and request.user.is_authenticated:


        website_serializer = WebSiteSerializer(data = request.data)
        if website_serializer.is_valid():
            labeled_website = add_website(website_serializer.data)
            labeled_website_serializer = LabeledWebSiteSerializer(labeled_website)
            return Response(labeled_website_serializer.data, status=status.HTTP_201_CREATED)

        return Response(website_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({}, status=status.HTTP_404_NOT_FOUND)
