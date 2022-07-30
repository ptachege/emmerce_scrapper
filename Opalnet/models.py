from django.db import models

# Create your models here.

class OpalnetCategories(models.Model):
    link = models.CharField(max_length=2000, blank=True,
                            null=True, unique=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'OpalnetCategories'
        verbose_name_plural = 'OpalnetCategories'


class OpalnetProductLinks(models.Model):
    link = models.CharField(max_length=2000, blank=True,
                            null=True, unique=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'OpalnetProductLinks'
        verbose_name_plural = 'OpalnetProductLinks'


class OpalnetFinalProducts(models.Model):
    product_name = models.CharField(
        max_length=20000, blank=True, null=True)
    product_price = models.CharField(max_length=20000, blank=True, null=True)
    regular_price = models.CharField(max_length=20000, blank=True, null=True)
    stock_status = models.CharField(max_length=20000, blank=True, null=True)
    sku = models.CharField(max_length=20000, blank=True, null=True)
    product_link = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.product_name

    class Meta:

        verbose_name = 'OpalnetFinalProducts'
        verbose_name_plural = 'OpalnetFinalProducts'
