from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.filters import (GlobalSearchFilter, ProductFilter, SaleFilter,
                         ShopFilter,)
from api.serializers import (ForecastSerializer, ProductSerializer,
                             SaleSerializer, ShopSerializer,)

from sales.models import Forecast, Product, Sale, Shop


class ProductViewSet(ModelViewSet):
    """
    Представление для работы с продуктами.

    Сериализатор: ProductSerializer
    Фильтры: ProductFilter (см. filters.py)
    Поиск: по полям name, sku, uom
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter,]
    filterset_class = ProductFilter


class SaleViewSet(ModelViewSet):
    """
    Представление для работы с продажами.

    Сериализатор: SaleSerializer
    Фильтры: SaleFilter (см. filters.py)
    Поиск: по полям store__name и sku
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter,]
    filterset_class = SaleFilter
    search_fields = ['store__name', 'sku']


class ShopViewSet(ModelViewSet):
    """
    Представление для работы с магазинами.

    Сериализатор: ShopSerializer
    Фильтры: ShopFilter (см. filters.py)
    Поиск: по полям city и type_format
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter,]
    filterset_class = ShopFilter
    search_fields = ['city', 'type_format']


class ForecastViewSet(ModelViewSet):
    """
    Представление для работы с прогнозами.

    Сериализатор: ForecastSerializer
    """
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter, GlobalSearchFilter]
