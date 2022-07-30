from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(HotpointCategories)
class HotpointCategories(admin.ModelAdmin):
    list_display = ("link", "crawled")


@admin.register(HotpointProductLinks)
class HotpointProductLinks(admin.ModelAdmin):
    list_display = ("link", "crawled")


admin.site.register(HotpointProducts)
