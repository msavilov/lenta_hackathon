from rest_framework import serializers

from sales.models import Forecast, Product, Sale, SaleFact, Shop


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Возвращает поля:
    - sku: id продукта.
    - group: Группа продукта.
    - category: Категория продукта.
    - subcategory: Подкатегория продукта.
    - uom: Единица измерения продукта.
    """
    group = serializers.ReadOnlyField(source='subcategory.category.group.name')
    category = serializers.ReadOnlyField(source='subcategory.category.name')
    subcategory = serializers.ReadOnlyField(source='subcategory.name')

    class Meta:
        model = Product
        fields = ('sku', 'group', 'category', 'subcategory', 'uom')


class SaleFactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SaleFact.

    Возвращает поля:
    - sale: Продажа, к которой относится данный факт продажи.
    - date: Дата факта продажи.
    - sales_type: Флаг наличия промо.
    - sales_units: Число проданных товаров без признака промо.
    - sales_units_promo: Число проданных товаров с признаком промо.
    - sales_rub: Продажи без признака промо в РУБ.
    - sales_run_promo: Продажи с признаком промо в РУБ.
    """

    class Meta:
        model = SaleFact
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Sale.

    Возвращает поля:
    - store: Магазин, в котором произошла продажа.
    - sku: id продукта.
    - facts: Факты продаж для данной продажи.
    """

    facts = SaleFactSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ('store', 'sku', 'facts')


class ShopSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Shop.

    Возвращает поля:
    - store: Название магазина.
    - city: Город, в котором находится магазин.
    - division: Подразделение магазина.
    - type_format: Формат магазина.
    - loc: Местоположение магазина.
    - size: Размер магазина.
    - is_active: Флаг активности магазина.
    """

    class Meta:
        model = Shop
        fields = '__all__'


class ForecastSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Forecast.

    Возвращает поля:
    - store: Магазин, к которому относится прогноз.
    - forecast_date: Дата прогноза.
    - forecast: Значение прогноза.
    """

    class Meta:
        model = Forecast
        fields = ('store', 'forecast_date', 'forecast',)
