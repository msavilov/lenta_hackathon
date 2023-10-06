from rest_framework import serializers

from api.models import Product, Forecast, Sale, Shop


class ProductSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='subcategory.category.group.name')
    category = serializers.ReadOnlyField(source='subcategory.category.name')
    subcategory = serializers.ReadOnlyField(source='subcategory.name')

    class Meta:
        model = Product
        fields = ('sku', 'group', 'category', 'subcategory', 'uom')


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
