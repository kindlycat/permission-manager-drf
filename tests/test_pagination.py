from unittest.mock import PropertyMock

import pytest
from rest_framework import status

from tests.app.models import TestModel
from tests.app.views import TestModelViewSet


@pytest.mark.django_db()
def test_default_list_actions(admin_client):
    response = admin_client.get(path='/model/')

    assert response.status_code == status.HTTP_200_OK
    assert 'permissions' not in response.json()


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ('client_name', 'expected_permissions'),
    [
        (
            'admin_client',
            {
                'create': {'allow': True, 'messages': None},
                'custom_non_detail': {'allow': True, 'messages': None},
            },
        ),
        (
            'user_client',
            {
                'create': {'allow': False, 'messages': None},
                'custom_non_detail': {
                    'allow': False,
                    'messages': ['Only staff can do it'],
                },
            },
        ),
    ],
)
def test_custom_list_actions(
    request,
    client_name,
    expected_permissions,
    mocker,
):
    mocker.patch.object(
        TestModelViewSet,
        attribute='permission_manager_list_actions',
        new_callable=PropertyMock,
        return_value=(
            'create',
            'custom_non_detail',
        ),
        create=True,
    )

    client = request.getfixturevalue(client_name)
    response = client.get(path='/model/')
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['permissions'] == expected_permissions


@pytest.mark.django_db()
def test_pagination_without_permission_manager(user_client, mocker):
    mocker.patch.object(
        TestModel,
        attribute='permission_manager',
        new_callable=PropertyMock,
        return_value=None,
    )
    mocker.patch.object(
        TestModelViewSet,
        attribute='permission_classes',
        new_callable=PropertyMock,
        return_value=[],
    )
    response = user_client.get(path='/model/')
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert 'permissions' not in data
