from django.db import models


class Group(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Группа товара'
    )

    class Meta:
        verbose_name = 'Группа товара'
        verbose_name_plural = 'Группы товаров'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Категория товара'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Подкатегория товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    class Meta:
        verbose_name = 'Подкатегория товара'
        verbose_name_plural = 'Подкатегории товара'

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(
        max_length=255,
        verbose_name='Захэшированное id'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Товар'
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE,
        related_name='products'
    )
    uom = models.PositiveIntegerField(
        verbose_name='Маркер, обозначающий продаётся товар на вес или в ШТ')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Shop(models.Model):
    store = models.CharField(
        max_length=50,
        verbose_name='Магазин'
    )
    city = models.CharField(
        max_length=50,
        verbose_name='Город'
    )
    division = models.CharField(
        max_length=50,
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
    store = models.CharField(max_length=100, verbose_name='Магазин')
    sku = models.CharField(
        max_length=50, verbose_name='Захэшированное id товара')
    facts = models.ManyToManyField(
        'SaleFact',
        related_name='sales',
        verbose_name='Факты продаж'
    )

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'


class SaleFact(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE,
        related_name='facts',
        verbose_name='Продажа'
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
        verbose_name = 'Факт продажи'
        verbose_name_plural = 'Факты продаж'
        ordering = ('-date', )

    def __str__(self):
        return (f'Факт продажи для Продажи {self.sale.sku}'
                f'в {self.sale.store} на {self.date}')
