from django.shortcuts import render, redirect
from .models import *

from django.forms import modelformset_factory
from .bullshit_detector import evaluate_website
from .forms import TaintedLemmaForm

TaintedLemmaFormSet = modelformset_factory(TaintedLemma, form=TaintedLemmaForm, extra=0)

# Create your views here.
def index(request):
    if request.POST:
        url = request.POST.get('website_url')
        if url:
            evaluate_website(url)

    lemmas_to_evaluate_query = TaintedLemma.objects.filter(is_evaluated=False)[:10]


    not_evaluated_lemmas_count = TaintedLemma.objects.filter(is_evaluated=False).count()



    lemmas_to_evaluate = TaintedLemma.objects.filter(id__in=lemmas_to_evaluate_query)

    formset = TaintedLemmaFormSet(queryset=lemmas_to_evaluate)
    context = {"formset": formset, 'not_evaluated_lemmas_count': not_evaluated_lemmas_count}

    return render(request, "bullshit_o_metre/index.html", context)

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
