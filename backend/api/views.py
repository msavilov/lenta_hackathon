from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.filters import SaleFilter, ShopFilter
from api.serializers import (ForecastSerializer, ProductSerializer,
                             SaleSerializer, ShopSerializer)
from sales.models import Forecast, Product, Sale, Shop


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [
        DjangoFilterBackend, SearchFilter]
    filterset_class = SaleFilter
    search_fields = ['store__name', 'sku']


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [
        django_filters.DjangoFilterBackend, SearchFilter]
    filterset_class = ShopFilter
    search_fields = ['city', 'loc']


class ForecastViewSet(ModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
