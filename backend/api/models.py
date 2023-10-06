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


class Forecast(models.Model):
    store = models.CharField(
        max_length=255,
        verbose_name='Магазин'
    )
    forecast_date = models.DateField(
        verbose_name='Дата прогноза'
    )
    forecast = models.JSONField(
        verbose_name='Прогноз'
    )

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'

    def __str__(self):
        return f'{self.store} - {self.forecast_date}'
