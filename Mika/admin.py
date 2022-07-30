from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(MikaCategories)
class MikaCategories(admin.ModelAdmin):
    list_display = ("link", "crawled")


@admin.register(MikaProductLinks)
class MikaProductLinks(admin.ModelAdmin):
    list_display = ("link", "crawled")


admin.site.register(MikaFinalProducts)
