from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name='Группа')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Подкатегория')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=255, verbose_name='SKU')
    name = models.CharField(max_length=255, verbose_name='Товар')
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name='products')
    uom = models.PositiveIntegerField(verbose_name='UOM')

    def __str__(self):
        return self.name


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
