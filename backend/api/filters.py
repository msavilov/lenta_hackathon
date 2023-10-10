from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet, NumberFilter,)

from sales.models import Product, Sale, Shop


class SaleFilter(FilterSet):
    """
    Фильтр для модели Sale.

    Поля фильтрации:
    - store: Магазин, по которому выполняется фильтрация
    (частичное совпадение).
    - sku: id продукта, по которому выполняется фильтрация.
    Пример:
    /api/sales/?store__name__icontains=Магазин1&sku=12345
    /api/sales/?sku=54321
    """
    store = CharFilter(field_name='store__name', lookup_expr='icontains')
    sku = CharFilter(field_name='sku')

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
    Примеры:
    /api/shops/?city__icontains=Город1&type_format=Крупный
    /api/shops/?city__icontains=Город2&is_active=true
    """
    city = CharFilter(lookup_expr='icontains')
    type_format = CharFilter(field_name='type_format')
    is_active = BooleanFilter(field_name='is_active')

    class Meta:
        model = Shop
        fields = ('city', 'type_format', 'is_active',)


class ProductFilter(FilterSet):
    """
    Фильтр для модели Product.

    Поля фильтрации:
    - name: Название товара, по которому выполняется фильтрация
    (частичное совпадение).
    - sku: Захэшированное id товара, по которому выполняется фильтрация.
    - uom: Маркер, обозначающий продаётся товар на вес или в ШТ.
    Пример:
    /api/products/?name__icontains=Товар1&sku=12345&uom=1
    """
    name = CharFilter(field_name='name', lookup_expr='icontains')
    sku = CharFilter(field_name='sku')
    uom = NumberFilter(field_name='uom')

    class Meta:
        model = Product
        fields = ('name', 'sku', 'uom',)


class GlobalSearchFilter(FilterSet):
    search = CharFilter(method='custom_search')

    def custom_search(self, queryset, name, value):
        sale_filter = SaleFilter(data=self.data, queryset=Sale.objects.all())
        shop_filter = ShopFilter(data=self.data, queryset=Shop.objects.all())
        product_filter = ProductFilter(
            data=self.data, queryset=Product.objects.all())

        sale_queryset = sale_filter.qs
        shop_queryset = shop_filter.qs
        product_queryset = product_filter.qs

        combined_queryset = (sale_queryset | shop_queryset
                             | product_queryset).distinct()
        return combined_queryset
