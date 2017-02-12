import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    started = models.DateTimeField('date started')
    last_active = models.DateTimeField('last active')
    address = models.CharField(max_length=500)
    postcode = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    reputation = models.BigIntegerField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Gear(models.Model):
    id = models.BigAutoField(primary_key=True)
    added = models.DateTimeField('date added')
    manufacture_year = models.DateField('manufactured')
    owner_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=500)
    model = models.CharField(max_length=500)
    note = models.CharField(max_length=2000)
    tech_details = models.CharField(max_length=2000)
    qty = models.PositiveSmallIntegerField(default=1, null=False)
    rack_units = models.PositiveSmallIntegerField(null=True)
    serial_no = models.CharField(max_length=500)
    form_factor = models.CharField(max_length=20, choices=((0, 'rack'), (1, 'desktop')))
    state = models.CharField(max_length=20, choices=((0, 'bad'), (1, 'ok'), (2, 'mint')))

def upload_manual(instance, filename):
    return 'manuals/' + str(uuid.uuid4())

class Manual(models.Model):
    id = models.BigAutoField(primary_key=True)
    added_by = models.ForeignKey(Profile, on_delete=None)
    gear_id = models.ForeignKey(Gear, on_delete=None)
    description = models.CharField(max_length=2000)
    upload = models.FileField(upload_to=upload_manual)


def upload_gear_picture(instance, filename):
    return 'gear_pictures/' + str(uuid.uuid4())

class GearPictures(models.Model):
    id = models.BigAutoField(primary_key=True)
    gear_id = models.ForeignKey(Gear, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to=upload_gear_picture)
