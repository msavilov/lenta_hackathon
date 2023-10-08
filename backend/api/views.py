from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from api.serializers import (ProductSerializer, ForecastSerializer,
                             SaleSerializer,
                             ShopSerializer,)
from sales.models import Product, Forecast, Sale, Shop


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['store', 'sku']

    def get_queryset(self):
        queryset = Sale.objects.all()
        store = self.request.query_params.get('store')
        sku = self.request.query_params.get('sku')
        if store:
            queryset = queryset.filter(store=store)
        if sku:
            queryset = queryset.filter(sku=sku)
        return queryset


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'cat']

    def get_queryset(self):
        queryset = Shop.objects.all()
        city = self.request.query_params.get('city')
        cat = self.request.query_params.get('cat')
        if city:
            queryset = queryset.filter(city=city)
        if cat:
            queryset = queryset.filter(cat=cat)
        return queryset


class ForecastViewSet(ModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
