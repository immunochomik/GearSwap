from django.contrib import admin
from .models import Gear, GearImage

class GearImageInline(admin.TabularInline):
    model = GearImage

class GearAdmin(admin.ModelAdmin):

    inlines = [GearImageInline]

admin.site.register(Gear, GearAdmin)