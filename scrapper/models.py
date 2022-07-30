from django.db import models

# Create your models here.


class HotpointCategories2(models.Model):
    link = models.TextField(blank=True, null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HotpointCategories'
        verbose_name_plural = 'HotpointCategories'


class HypermartCategories2(models.Model):
    link = models.TextField(max_length=900, blank=True,
                            null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HypermartCategories'
        verbose_name_plural = 'HypermartCategories'


class MikaCategories2(models.Model):
    link = models.TextField(blank=True,
                            null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'MikaCategories'
        verbose_name_plural = 'MikaCategories'


class OpalnetCategories2(models.Model):
    link = models.TextField(blank=True,
                            null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'OpalnetCategories'
        verbose_name_plural = 'OpalnetCategories'


# product links


class HotpointProductLinks2(models.Model):
    link = models.TextField(blank=True,
                            null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HotpointProductLinks'
        verbose_name_plural = 'HotpointProductLinks'


class HypermartProductLinks2(models.Model):
    link = models.TextField(blank=True,
                            null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'HypermartProductLinks'
        verbose_name_plural = 'HypermartProductLinks'


class MikaProductLinks2(models.Model):
    link = models.TextField(blank=True,
                            null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'MikaProductLinks'
        verbose_name_plural = 'MikaProductLinks'


class OpalnetProductLinks2(models.Model):
    link = models.TextField(blank=True,
                            null=True)
    crawled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.link)

    class Meta:
        verbose_name = 'OpalnetProductLinks'
        verbose_name_plural = 'OpalnetProductLinks'


class Products(models.Model):
    product_name = models.TextField(
        max_length=10000, blank=True, null=True)
    regular_price = models.TextField(max_length=10000, blank=True, null=True)
    sale_price = models.TextField(max_length=10000, blank=True, null=True)
    brand = models.TextField(max_length=10000, blank=True, null=True)
    upc = models.TextField(max_length=10000, blank=True, null=True)
    sku = models.TextField(max_length=10000, blank=True, null=True)
    product_link = models.TextField(blank=True, null=True)
    stock_status = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.product_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Products'
        verbose_name_plural = 'Products'
