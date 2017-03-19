from django.shortcuts import render
from actions.models import Action
from actions.utils import create_action
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.forms import modelformset_factory, inlineformset_factory
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action, prepare_acctions
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden
from .models import Gear, GearImage
from .forms import GearAddForm, GearImageForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@require_GET
def gear_list(request):
    paginator = Paginator(Gear.objects.all(), 5)
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
            messages.success(request, "You have adde an item")
            return HttpResponseRedirect(reverse('account:dashboard'))

    return render(request, 'gear/add.html',
                  {'gear_form': gear_form, 'form_set': form_set, 'action': reverse('gear:add') })


@login_required
def edit(request, gear_id):
    instance = get_object_or_404(Gear, id=gear_id)
    if instance.owner != request.user:
        return HttpResponseForbidden()
    ImageFormSet = inlineformset_factory(Gear, GearImage, fields=('image',))

    if request.method == 'POST':
        form_set = ImageFormSet(request.POST, request.FILES, instance=instance)
        gear_form = GearAddForm(request.POST, request.FILES, instance=instance)
        if gear_form.is_valid() and form_set.is_valid():
            gear_instance = gear_form.save(commit=False)
            gear_instance.save()
            form_set.save()
            messages.success(request, "You have edited an item")
            return HttpResponseRedirect(reverse('gear:details', kwargs={'gear_id': gear_id}))
    gear_form = GearAddForm(initial=model_to_dict(instance))
    form_set = ImageFormSet(instance=instance)
    return render(request, 'gear/add.html',
                  {'gear_form': gear_form, 'form_set': form_set, 'action': reverse('gear:edit',
                                                                                   kwargs={'gear_id':gear_id})})


@require_GET
def details(request, gear_id):
    return render(request, 'gear/details.html', {'item': get_object_or_404(Gear, id=gear_id)})


@login_required
def delete(request, gear_id):
    gear_instance = get_object_or_404(Gear, id=gear_id)
    if gear_instance.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'GET':
        return render(request, 'gear/delete.html', {'item': gear_instance})
    gear_instance.delete()
    create_action(request.user, 'Deleted gear', gear_instance)
    messages.success(request, "You have deleted an item")
    return HttpResponseRedirect(reverse('account:dashboard'))