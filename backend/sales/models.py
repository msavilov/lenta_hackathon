from django.conf import settings
from django.db import models


class Group(models.Model):
    """
    Модель, представляющая группу товаров.

    Attributes:
        name (str): Название группы товаров.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.

    Methods:
        __str__(): Возвращает строковое представление группы товаров.

    """
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
    """
    Модель, представляющая категорию товаров.

    Attributes:
        name (str): Название категории товаров.
        group (Group): Ссылка на группу товаров, к которой относится категория.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.

    Methods:
        __str__(): Возвращает строковое представление категории товаров.

    """
    name = models.CharField(
        max_length=settings.LONG_NAME_LENGTH,
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
    """
    Модель, представляющая подкатегорию товаров.

    Attributes:
        name (str): Название подкатегории товаров.
        category (Category): Ссылка на категорию товаров, к которой
        относится подкатегория.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.

    Methods:
        __str__(): Возвращает строковое представление подкатегории товаров.

    """
    name = models.CharField(
        max_length=settings.LONG_NAME_LENGTH,
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
    """
    Модель, представляющая товар.

    Attributes:
        sku (str): Захэшированный идентификатор товара.
        name (str): Название товара.
        subcategory (Subcategory): Ссылка на подкатегорию товара.
        uom (int): Маркер, обозначающий, продается товар на вес или в штуках.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.

    Methods:
        __str__(): Возвращает строковое представление товара.

    """
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

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Shop(models.Model):
    """
    Модель, представляющая магазин.

    Attributes:
        store (str): Название магазина.
        city (str): Город, в котором расположен магазин.
        division (str): Подразделение магазина.
        type_format (int): Формат магазина.
        loc (int): Тип локации/окружения магазина.
        size (int): Тип размера магазина.
        is_active (int): Флаг активности магазина.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.

    Methods:
        __str__(): Возвращает строковое представление магазина.

    """
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
    loc = models.IntegerField(verbose_name='Тип локации/окружения магазина')
    size = models.IntegerField(verbose_name='Тип размера магазина')
    is_active = models.IntegerField(verbose_name='Активен')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.store


class Forecast(models.Model):
    """
    Модель, представляющая прогноз продаж для магазина.

    Attributes:
        store (Shop): Ссылка на магазин, для которого составлен прогноз.
        forecast_date (Date): Дата прогноза.
        forecast (JSONField): Прогноз продаж в формате JSON.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.

    Methods:
        __str__(): Возвращает строковое представление прогноза.

    """
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
    """
    Модель, представляющая информацию о продажах.

    Attributes:
        store (Shop): Ссылка на магазин, в котором произошла продажа.
        sku (str): Захэшированный идентификатор товара.
        facts (ManyToManyField): Связь с фактами продаж.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.

    Methods:
        __str__(): Возвращает строковое представление объекта Sale, которое
        включает информацию о магазине и товара.

    """
    store = models.ForeignKey(
        Shop, on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Магазин'
    )
    sku = models.CharField(
        max_length=50, verbose_name='Захэшированное id товара')
    facts = models.ManyToManyField(
        'SaleFact',
        related_name='sales_related',
        verbose_name='Факты продаж'
    )

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

    def __str__(self):
        return f'Продажа в магазине {self.store} (Товар: {self.sku})'


class SaleFact(models.Model):
    """
    Модель, представляющая факт продажи товара.

    Attributes:
        sale (Sale): Ссылка на продажу, к которой относится факт продажи.
        date (Date): Дата продажи.
        sales_type (int): Флаг наличия промо.
        sales_units (int): Число проданных товаров без признака промо.
        sales_units_promo (int): Число проданных товаров с признаком промо.
        sales_rub (float): Продажи без признака промо в рублях.
        sales_run_promo (float): Продажи с признаком промо в рублях.

    Meta:
        verbose_name (str): Имя для отображения в административной панели.
        verbose_name_plural (str): Имя во множественном числе для отображения
        в административной панели.
        ordering (tuple): Спецификация порядка сортировки записей.

    Methods:
        __str__(): Возвращает строковое представление факта продажи.

    """
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE,
        related_name='sales_facts',
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
