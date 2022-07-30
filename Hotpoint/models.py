from tokenize import blank_re
from django.db import models

# Create your models here.


class HotpointCategories(models.Model):
    link = models.CharField(max_length=2000, blank=True, null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HotpointCategories'
        verbose_name_plural = 'HotpointCategories'


class HotpointProductLinks(models.Model):
    link = models.CharField(max_length=2000, blank=True,
                            null=True, unique=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HotpointProductLinks'
        verbose_name_plural = 'HotpointProductLinks'


class HotpointProducts(models.Model):
    product_name = models.CharField(
        max_length=20000, blank=True, null=True)
    product_price = models.CharField(max_length=20000, blank=True, null=True)
    regular_price = models.CharField(max_length=20000, blank=True, null=True)
    brand = models.CharField(max_length=20000, blank=True, null=True)
    upc = models.CharField(max_length=20000, blank=True, null=True)
    sku = models.CharField(max_length=20000, blank=True, null=True)
    product_link = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'HotpointProducts'
        verbose_name_plural = 'HotpointProducts'
