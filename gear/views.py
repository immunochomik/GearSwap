from django.shortcuts import render
from actions.models import Action
from actions.utils import create_action
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.urls import reverse
from .models import Gear, GearImage
from .forms import GearAddForm, GearImageForm
import q
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def gear_list(request):
    pass


@login_required
def add(request):
    ImageFormSet = modelformset_factory(GearImage, form=GearImageForm, extra=3)
    form_set = ImageFormSet(queryset=GearImage.objects.none())
    gear_form = GearAddForm(request.POST)

    if request.method == 'POST':
        form_set = ImageFormSet(request.POST, request.FILES,
                            queryset=GearImage.objects.none())

        if gear_form.is_valid() and form_set.is_valid():
            from datetime import datetime
            gear_instance = gear_form.save(commit=False)
            gear_instance.owner = request.user
            gear_instance.added = datetime.now()
            gear_instance.save()

            for form in form_set.cleaned_data:
                image = form.get('image')
                if not image:
                    continue
                photo = GearImage(gear=gear_instance, image=image)
                photo.save()

            messages.success(request, "Yeeew,check it out on the home page!")
            return HttpResponseRedirect(reverse('account:dashboard'))

    return render(request, 'gear/add.html',
                  {'gear_form': gear_form, 'form_set': form_set})


def edit(request):
    pass


def delete(request):
    pass