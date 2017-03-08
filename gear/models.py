import uuid
import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError


def year_choices(n = 10):
    return tuple(zip([i for i in range(0, n)],[y for y in range(2018 - n, 2018)]))


def upload_gear_image(instance, filename):
    return 'gear_images/{0}.{1}'.format(
        str(uuid.uuid4()),
        filename.rsplit('.', 1)[1])

def validate_image(fieldfile_obj):
    megabyte_limit = 2
    if  fieldfile_obj.file.size > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

class Gear(models.Model):
    id = models.BigAutoField(primary_key=True)
    added = models.DateTimeField('date added')
    manufacture_year = models.PositiveSmallIntegerField(choices=year_choices(50))
    slug = models.SlugField(max_length=200, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='gear_owned',
                                 on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=500)
    model = models.CharField(max_length=500)
    note = models.CharField(max_length=2000)
    tech_details = models.CharField(max_length=2000)
    qty = models.PositiveSmallIntegerField(default=1, null=False)
    rack_units = models.PositiveSmallIntegerField(null=True)
    serial_no = models.CharField(max_length=500)
    form_factor = models.PositiveSmallIntegerField(choices=((0, 'rack'), (1, 'desktop')))
    state = models.PositiveSmallIntegerField(choices=((0, 'bad'), (1, 'ok'), (2, 'mint')))
    main_image = models.ImageField(upload_to=upload_gear_image, validators=[validate_image])


class GearImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    gear = models.ForeignKey(Gear, on_delete=models.CASCADE,
                                related_name='gear_image')
    image = models.ImageField(upload_to=upload_gear_image, validators=[validate_image])


def upload_manual(instance, filename):
    return 'manuals/' + str(uuid.uuid4())

class Manual(models.Model):
    id = models.BigAutoField(primary_key=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='manuals_added',
                                on_delete=None)
    gear_id = models.ForeignKey(Gear, on_delete=None, related_name='manuals')
    description = models.CharField(max_length=2000)
    slug = models.SlugField(max_length=200, blank=True)
    upload = models.FileField(upload_to=upload_manual)



