from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

from django.forms import modelformset_factory
from .bullshit_detector import evaluate_website
from .forms import TaintedLemmaForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

TaintedLemmaFormSet = modelformset_factory(TaintedLemma, form=TaintedLemmaForm, extra=0)

# Create your views here.
@login_required(login_url="index")
def index(request):
    if request.POST:
        url = request.POST.get('website_url')
        if url:
            evaluate_website(url)

    lemmas_to_evaluate_query = TaintedLemma.objects.filter(is_evaluated=False)[:50]


    not_evaluated_lemmas_count = TaintedLemma.objects.filter(is_evaluated=False).count()



    lemmas_to_evaluate = TaintedLemma.objects.filter(id__in=lemmas_to_evaluate_query)

    formset = TaintedLemmaFormSet(queryset=lemmas_to_evaluate)
    context = {"formset": formset, 'not_evaluated_lemmas_count': not_evaluated_lemmas_count}

    return render(request, "bullshit_o_metre/index.html", context)

@login_required(login_url="index")
def evaluate_tainted_lemmas(request):
    if request.method == "POST":

        formset = TaintedLemmaFormSet(request.POST)
        if formset.is_valid():
            print("oki")
            formset.save()
            print("valid")
        else:
            print(formset.errors)

    return redirect('bullshit_index')

@api_view(['POST'])
def website(request):
    url = request.GET.get('url')
    recalculate = request.GET.get('recalculate') == 'true'
    print(recalculate)

    if "http" not in url:
        return Response({'error': 'url not valid', 'error_no': '1'})

    print(url)

    website = evaluate_website(url, recalculate)

    serializer = RecordedWebSiteSerializer(website)
    return Response(serializer.data)
