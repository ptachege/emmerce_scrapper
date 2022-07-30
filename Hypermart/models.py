from django.db import models

# Create your models here.


class HypermartCategories(models.Model):
    link = models.CharField(max_length=2000, blank=True,
                            null=True, unique=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HypermartCategories'
        verbose_name_plural = 'HypermartCategories'


class HypermartProductLinks(models.Model):
    link = models.CharField(max_length=2000, blank=True,
                            null=True, unique=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HypermartProductLinks'
        verbose_name_plural = 'HypermartProductLinks'


class HypermartProducts(models.Model):
    product_name = models.CharField(
        max_length=20000, blank=True, null=True)
    product_price = models.CharField(max_length=20000, blank=True, null=True)
    regular_price = models.CharField(max_length=20000, blank=True, null=True)
    brand = models.CharField(max_length=20000, blank=True, null=True)
    sku = models.CharField(max_length=20000, blank=True, null=True)
    product_link = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'HypermartProducts'
        verbose_name_plural = 'HypermartProducts'
