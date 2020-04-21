from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SentenceSerializer
from .models import *

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        "list sentences": "/sentences/"
    }
    return Response(api_urls)

@api_view(['GET', 'POST', 'DELETE'])
def sentences(request):
    if request.method == "GET":
        sentences = Sentence.objects.all()
        serializer = SentenceSerializer(sentences, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        return Response({"message": "sentence created!"})
    elif request.method == "DELETE":
        return Response({"message": "sentence deleted"})
    else:
        return Response({"message":"Protocol invalid!"})
