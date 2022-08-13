from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(HotpointCategories2)
class HotpointCategories(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(HotpointProductLinks2)
class HotpointProductLinks(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(HypermartCategories2)
class HypermartCategories(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(HypermartProductLinks2)
class HypermartProductLinks(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(MikaCategories2)
class MikaCategories(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(MikaProductLinks2)
class MikaProductLinks(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(OpalnetCategories2)
class OpalnetCategories(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(OpalnetProductLinks2)
class OpalnetProductLinks(ImportExportModelAdmin):
    list_display = ("link", "crawled")


@admin.register(Products)
class Products(ImportExportModelAdmin):
    list_display = ("sku", "regular_price")

