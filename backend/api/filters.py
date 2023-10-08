from django_filters.rest_framework import FilterSet

from sales.models import Sale, Shop


class SaleFilter(FilterSet):
    """
    Фильтр для модели Sale.

    Поля фильтрации:
    - store: Магазин, по которому выполняется фильтрация.
    - sku: Артикул продукта, по которому выполняется фильтрация.
    """

    class Meta:
        model = Sale
        fields = ('store', 'sku',)


class ShopFilter(FilterSet):
    """
    Фильтр для модели Shop.

    Поля фильтрации:
    - city: Город, по которому выполняется фильтрация.
    - type_format: Формат магазина, по которому выполняется фильтрация.
    - is_active: Флаг активности магазина, по которому выполняется фильтрация.
    """

    class Meta:
        model = Shop
        fields = ('city', 'type_format', 'is_active',)
