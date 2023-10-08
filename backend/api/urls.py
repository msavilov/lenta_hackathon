from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import ForecastViewSet, ProductViewSet, SaleViewSet, ShopViewSet

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.yourapi.com/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


v1_router = DefaultRouter()
v1_router.register('categories', ProductViewSet, basename='categories')
v1_router.register('sales', SaleViewSet, basename='tasalesgs')
v1_router.register('shops', ShopViewSet, basename='shops')
v1_router.register('forecast', ForecastViewSet, basename='forecast')


urlpatterns = [
    path('', include(v1_router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]
