from rest_framework import serializers

from api.models import Category, Forecast, Sale, SalesUnit, Shop


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


class SalesUnitsSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(max_length=50)
    sales_units = serializers.DictField(child=serializers.IntegerField())

    class Meta:
        model = SalesUnit
        fields = ('sku', 'sales_units')


class ForecastSerializer(serializers.ModelSerializer):
    store = serializers.CharField(max_length=50)
    forecast_date = serializers.DateField()
    forecast = SalesUnitsSerializer()

    class Meta:
        model = Forecast
        fields = ('store', 'forecast_date', 'forecast')
