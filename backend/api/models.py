from django.db import models


class Category(models.Model):
    sku = models.CharField(max_length=50)
    group = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    uom = models.IntegerField()

    def __str__(self):
        return self.sku


class Sale(models.Model):
    store = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    date = models.DateField()
    sales_type = models.IntegerField()
    sales_units = models.IntegerField()
    sales_units_promo = models.IntegerField()
    sales_rub = models.FloatField()
    sales_run_promo = models.FloatField()


class Shop(models.Model):
    store = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    type_format = models.IntegerField()
    loc = models.IntegerField()
    size = models.IntegerField()
    is_active = models.BooleanField()


class SalesUnit(models.Model):
    forecast = models.ForeignKey(
        'Forecast', related_name='sales_units', on_delete=models.CASCADE)
    date = models.DateField()
    sku = models.CharField(max_length=50)
    sales_units = models.IntegerField()


class Forecast(models.Model):
    store = models.CharField(max_length=50)
    forecast_date = models.DateField()
