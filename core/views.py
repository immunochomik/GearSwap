from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader

# Create your views here.

def index(request):
    template = loader.get_template('core/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
    