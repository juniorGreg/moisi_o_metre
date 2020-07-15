from django.shortcuts import render
from .models import *

from django.forms import modelformset_factory
from .bullshit_detector import evaluate_website


TaintedLemmaFormSet = modelformset_factory(TaintedLemma, fields='__all__')

# Create your views here.
def index(request):
    if request.POST:
        url = request.POST.get('website_url')
        if url:
            evaluate_website(url)

    lemmas_to_evaluate = TaintedLemma.objects.filter(is_evaluated=False)[:20].update(read=True)

    formset = TaintedLemmaFormSet(queryset=lemmas_to_evaluate)
    context = {"formset": formset}

    return render(request, "bullshit_o_metre/index.html", context)

def evaluate_tainted_lemmas(request):
    formset = TaintedLemmaFormSet(request.POST)
    if formset.is_valid():
        formset.save()
