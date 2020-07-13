from django.shortcuts import render
from .models import *
from .forms import TaintedLemmaForm
from django.forms import formset_factory

TaintedLemmaFormSet = formset_factory(TaintedLemmaForm)

# Create your views here.
def index(request):
    if request.POST:
        url = request.POST.get('website_url')
        if url:
            print(url)
    lemmas_to_evaluate = TaintedLemma.objects.filter(is_evaluated=False)
    formset = TaintedLemmaFormSet(lemmas_to_evaluate)
    context = {"formset": formset}

    return render(request, "bullshit_o_metre/index.html", context)

def evaluate_tainted_lemmas(request):
    formset = TaintedLemmaFormSet(request.POST)
    if formset.is_valid():
        formset.save()
