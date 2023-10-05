from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Category, Forecast, Sale, Shop
from api.serializers import (CategorySerializer, ForecastSerializer,
                             SaleSerializer, SalesUnitsSerializer,
                             ShopSerializer)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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

    def create(self, request, *args, **kwargs):
        data = request.data.get('data', None)
        if data is not None:
            forecasts = []
            for item in data:
                sales_units_data = item.get(
                    'forecast', {}).get('sales_units', {})
                forecast_data = {
                    'store': item.get('store'),
                    'forecast_date': item.get('forecast_date')
                }
                forecast_serializer = ForecastSerializer(data=forecast_data)
                if forecast_serializer.is_valid():
                    forecast = forecast_serializer.save()
                    for date, sales_units in sales_units_data.items():
                        sales_unit_data = {
                            'sku': item.get('forecast', {}).get('sku'),
                            'sales_units': sales_units,
                            'date': date
                        }
                        sales_unit_serializer = SalesUnitsSerializer(
                            data=sales_unit_data)
                        if sales_unit_serializer.is_valid():
                            sales_unit_serializer.save(forecast=forecast)
                        else:
                            forecast.delete()
                            return Response(sales_unit_serializer.errors,
                                            status=status.HTTP_400_BAD_REQUEST)
                    forecasts.append(forecast)
                else:
                    return Response(forecast_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response(ForecastSerializer(forecasts, many=True).data,
                            status=status.HTTP_201_CREATED)
        return Response({'detail': "Invalid data format"},
                        status=status.HTTP_400_BAD_REQUEST)
