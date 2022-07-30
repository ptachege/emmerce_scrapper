from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(HypermartCategories)
class HypermartCategories(admin.ModelAdmin):
    list_display = ("link", "crawled")



@admin.register(HypermartProductLinks)
class HypermartProductLinks(admin.ModelAdmin):
    list_display = ("link", "crawled")


admin.site.register(HypermartProducts)
