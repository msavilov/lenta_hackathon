from django.conf import settings
from django.db import models


class Group(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Группа товара'
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=settings.LONG_NAME_LENGTH,
        verbose_name='Категория товара'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(
        max_length=settings.LONG_NAME_LENGTH,
        verbose_name='Подкатегория товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(
        max_length=settings.LONG_NAME_LENGTH,
        verbose_name='Захэшированное id'
    )
    name = models.CharField(
        max_length=settings.LONG_NAME_LENGTH,
        verbose_name='Товар'
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE,
        related_name='products'
    )
    uom = models.PositiveIntegerField(
        verbose_name='Маркер, обозначающий продаётся товар на вес или в ШТ')

    def __str__(self):
        return self.name


class Shop(models.Model):
    store = models.CharField(
        max_length=settings.SHORT_NAME_LENGTH,
        verbose_name='Магазин'
    )
    city = models.CharField(
        max_length=settings.SHORT_NAME_LENGTH,
        verbose_name='Город'
    )
    division = models.CharField(
        max_length=settings.SHORT_NAME_LENGTH,
        verbose_name='Подразделение'
    )
    type_format = models.IntegerField(verbose_name='Формат')
    loc = models.IntegerField(verbose_name='Местоположение')
    size = models.IntegerField(verbose_name='Размер')
    is_active = models.BooleanField(verbose_name='Активен')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.store


class Forecast(models.Model):
    store = models.ForeignKey(
        Shop, on_delete=models.CASCADE,
        related_name='forecasts',
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


class Sale(models.Model):
    store = models.ForeignKey(
        Shop, on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Магазин'
    )
    sku = models.CharField(
        max_length=50,
        verbose_name='Захэшированное id'
    )
    date = models.DateField(verbose_name='Дата')
    sales_type = models.IntegerField(verbose_name='Флаг наличия промо')
    sales_units = models.IntegerField(
        verbose_name='Число проданных товаров без признака промо')
    sales_units_promo = models.IntegerField(
        verbose_name='Число проданных товаров с признаком промо')
    sales_rub = models.FloatField(
        verbose_name='Продажи без признака промо в РУБ')
    sales_run_promo = models.FloatField(
        verbose_name='Продажи с признаком промо в РУБ')

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

    def __str__(self):
        return f'Sale {self.sku} at {self.store} on {self.date}'
