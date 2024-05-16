import pytest
from rest_framework import status

from tests.app.models import TestModel, TestModelStatus


@pytest.mark.django_db()
def test_create_positive(admin_client):
    initial_count = TestModel.objects.count()
    response = admin_client.post(
        path='/model/',
        data={
            'title': 'Test',
            'status': TestModelStatus.DRAFT,
        },
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert TestModel.objects.count() == initial_count + 1


@pytest.mark.django_db()
def test_create_negative(user_client):
    initial_count = TestModel.objects.count()
    response = user_client.post(
        path='/model/',
        data={
            'title': 'Test',
            'status': TestModelStatus.DRAFT,
        },
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert TestModel.objects.count() == initial_count


@pytest.mark.django_db()
@pytest.mark.parametrize('method', ['put', 'patch'])
def test_update_positive(admin_client, method):
    instance = TestModel.objects.create(title='Test')

    response = getattr(admin_client, method)(
        path=f'/model/{instance.pk}/',
        data={
            'title': method,
            'status': TestModelStatus.DRAFT,
        },
        content_type='application/json',
    )

    instance.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert instance.title == method


@pytest.mark.django_db()
@pytest.mark.parametrize('method', ['put', 'patch'])
def test_update_negative(user_client, method):
    instance = TestModel.objects.create(title='Test')

    response = getattr(user_client, method)(
        path=f'/model/{instance.pk}/',
        data={
            'title': method,
            'status': TestModelStatus.DRAFT,
        },
        content_type='application/json',
    )

    instance.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert instance.title == 'Test'


@pytest.mark.django_db()
def test_delete_positive(admin_client):
    instance = TestModel.objects.create(title='Test')
    initial_count = TestModel.objects.count()

    response = admin_client.delete(path=f'/model/{instance.pk}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert TestModel.objects.count() == initial_count - 1


@pytest.mark.django_db()
def test_delete_negative(user_client):
    instance = TestModel.objects.create(title='Test')
    initial_count = TestModel.objects.count()

    response = user_client.delete(path=f'/model/{instance.pk}/')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert TestModel.objects.count() == initial_count


@pytest.mark.django_db()
@pytest.mark.parametrize('client_name', ['admin_client', 'user_client'])
def test_list_positive(request, client_name):
    instance = TestModel.objects.create(title='Test')

    client = request.getfixturevalue(client_name)
    response = client.get(path='/model/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'][0]['title'] == instance.title


@pytest.mark.django_db()
@pytest.mark.parametrize('client_name', ['admin_client', 'user_client'])
def test_view_positive(request, client_name):
    instance = TestModel.objects.create(
        title='Test', status=TestModelStatus.PUBLISHED
    )

    client = request.getfixturevalue(client_name)
    response = client.get(path=f'/model/{instance.pk}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == instance.title


@pytest.mark.django_db()
def test_view_negative(user_client):
    instance = TestModel.objects.create(title='Test')

    response = user_client.get(path=f'/model/{instance.pk}/')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
def test_publish_positive(admin_client):
    instance = TestModel.objects.create(title='Test')

    response = admin_client.patch(path=f'/model/{instance.pk}/publish/')

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ('client_name', 'instance_status'),
    [
        ('admin_client', TestModelStatus.PUBLISHED),
        ('user_client', TestModelStatus.DRAFT),
        ('user_client', TestModelStatus.PUBLISHED),
    ],
)
def test_publish_negative(request, client_name, instance_status):
    instance = TestModel.objects.create(title='Test', status=instance_status)

    client = request.getfixturevalue(client_name)
    response = client.patch(path=f'/model/{instance.pk}/publish/')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
def test_custom_non_detail_positive(admin_client):
    response = admin_client.get(path='/model/custom_non_detail/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'custom_non_detail': True}


@pytest.mark.django_db()
def test_custom_non_detail_negative(user_client):
    response = user_client.get(path='/model/custom_non_detail/')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
def test_view_without_action_negative(admin_client):
    instance = TestModel.objects.create(title='Test')

    response = admin_client.patch(path=f'/model/{instance.pk}/without_action/')
    assert response.status_code == status.HTTP_200_OK
