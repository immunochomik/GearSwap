from django.shortcuts import render
from actions.models import Action
from actions.utils import create_action
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action, prepare_acctions
from .models import Gear, GearImage
from .forms import GearAddForm, GearImageForm
import q
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def gear_list(request):
    paginator = Paginator(Gear.objects.all(), 3)
    try:
        gear_items = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        gear_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        gear_items = paginator.page(paginator.num_pages)
    return render(request, 'gear/list.html', {
        'actions': prepare_acctions(),
        'gear_items': gear_items})


@login_required
def add(request):
    ImageFormSet = modelformset_factory(GearImage, form=GearImageForm, extra=3)
    form_set = ImageFormSet(queryset=GearImage.objects.none())
    gear_form = GearAddForm(request.POST, request.FILES)

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

            create_action(request.user, 'added gear', gear_instance)
            messages.success(request, "Yeeew,check it out on the home page!")
            return HttpResponseRedirect(reverse('account:dashboard'))

    return render(request, 'gear/add.html',
                  {'gear_form': gear_form, 'form_set': form_set})


def edit(request):
    pass


def delete(request):
    pass