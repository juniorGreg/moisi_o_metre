from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

from django.forms import modelformset_factory
from .bullshit_detector_api import *


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


# Create your views here.
@login_required(login_url="index")
def index(request):

    labeled_website_count = LabeledWebSite.objects.count()
    bullshit_labeled_website_count = LabeledWebSite.objects.filter(is_bullshit=True).count()
    no_bullshit_labeled_website_count = LabeledWebSite.objects.filter(is_bullshit=False).count()

    context = {"labeled_website_count": labeled_website_count,
                "bullshit_labeled_website_count": bullshit_labeled_website_count,
                "no_bullshit_labeled_website_count": no_bullshit_labeled_website_count}

    return render(request, "bullshit_o_metre/index.html", context)



@api_view(['PUT', 'POST'])
def website(request):
    def get_error_dict(message):
        return {'message': message }

    if request.method == "PUT":
        data = request.data
        print(data)

        if data["url"]:
            url = data["url"]
            if "http" not in url:
                return Response(get_error_dict("L'adresse web n'est pas valid"), status=status.HTTP_400_BAD_REQUEST)

                print(url)

            try:
                title, score = evaluate_website(url)
            except TextTooShortException:
                return Response(get_error_dict("Le texte recupéré est trop court pour être évalué."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except YoutubeNoCaptionException:
                return Response(get_error_dict("Le vidéo Youtube n'a pas de transcription ou de soutitre en français."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except EncodingNotFoundException:
                return Response(get_error_dict("L'encodage du site est inconnu."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except InvalidLanguage:
                return Response(get_error_dict("Le site n'est pas en français."), status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response(get_error_dict("Une erreur s'est produite."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif data["text"]:
            title, score = evaluate_text(data["text"])


        return Response({'title': title, 'score': score})

    if request.method == "POST" and request.user.is_authenticated:


        website_serializer = WebSiteSerializer(data = request.data)
        if website_serializer.is_valid():
            labeled_website = add_website(website_serializer.data)
            labeled_website_serializer = LabeledWebSiteSerializer(labeled_website)
            return Response(labeled_website_serializer.data, status=status.HTTP_201_CREATED)

        return Response(website_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({}, status=status.HTTP_404_NOT_FOUND)
