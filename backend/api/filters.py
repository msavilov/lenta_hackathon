from django_filters.rest_framework import FilterSet

from sales.models import Sale, Shop


class SaleFilter(FilterSet):
    class Meta:
        model = Sale
        fields = ('store', 'sku',)


class ShopFilter(FilterSet):
    class Meta:
        model = Shop
        fields = ('city', 'type_format', 'is_active',)
