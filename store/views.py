from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from blog.views import get_main_context

# Create your views here.



def index(request):
    context = get_main_context("Boutique", "La boutique du MoisiOMètre", "/store")
    return render(request, "store/index.html", context)

@csrf_exempt
def webhook(request):
    return HttpResponse("success")

#API
import requests
API_PRINTFUL = "https://api.printful.com/%s"
HEADERS = {'Authorization': 'Basic %s' % settings.PRINTFUL_API_KEY }

@api_view(['GET'])
def products(request):
    r = requests.get(API_PRINTFUL % "store/products", headers=HEADERS)
    return Response(r.json())
