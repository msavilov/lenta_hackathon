from rest_framework import serializers

from sales.models import Forecast, Product, Sale, SaleFact, Shop


class ProductSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='subcategory.category.group.name')
    category = serializers.ReadOnlyField(source='subcategory.category.name')
    subcategory = serializers.ReadOnlyField(source='subcategory.name')

    class Meta:
        model = Product
        fields = ('sku', 'group', 'category', 'subcategory', 'uom')


class SaleFactSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleFact
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    facts = SaleFactSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ('store', 'sku', 'facts')


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'


class ForecastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forecast
        fields = ('store', 'forecast_date', 'forecast',)
