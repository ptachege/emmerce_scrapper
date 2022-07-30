from django.db import models

# Create your models here.


class MikaCategories(models.Model):
    link = models.CharField(max_length=2000, blank=True,
                            null=True, unique=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'MikaCategories'
        verbose_name_plural = 'MikaCategories'


class MikaProductLinks(models.Model):
    link = models.CharField(max_length=2000, blank=True,
                            null=True, unique=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'MikaProductLinks'
        verbose_name_plural = 'MikaProductLinks'



class MikaFinalProducts(models.Model):
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

        verbose_name = 'MikaFinalProducts'
        verbose_name_plural = 'MikaFinalProductss'
