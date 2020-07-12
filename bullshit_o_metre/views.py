from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "bullshit_o_metre/index.html")
