from rest_framework import serializers

from api.models import Category, Forecast, Sale, Shop


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ForecastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forecast
        fields = ('store', 'forecast_date', 'forecast',)
