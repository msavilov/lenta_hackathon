import pytest
from rest_framework.test import APIClient
from rest_framework import status

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client():
    user = User.objects.create_user(
        email='testuser@example.com', password='testpassword')
    return user


@pytest.mark.django_db
def test_product_endpoint(api_client):
    url = '/categories/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_product_endpoint_authenticated(api_client, authenticated_api_client):
    api_client.force_authenticate(user=authenticated_api_client)
    url = '/categories/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_sale_endpoint(api_client):
    url = '/sales/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_sale_endpoint_authenticated(api_client, authenticated_api_client):
    api_client.force_authenticate(user=authenticated_api_client)
    url = '/sales/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_shop_endpoint(api_client):
    url = '/shops/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_shop_endpoint_authenticated(api_client, authenticated_api_client):
    api_client.force_authenticate(user=authenticated_api_client)
    url = '/shops/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_forecast_endpoint(api_client):
    url = '/forecast/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_forecast_endpoint_authenticated(api_client, authenticated_api_client):
    api_client.force_authenticate(user=authenticated_api_client)
    url = '/forecast/'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
