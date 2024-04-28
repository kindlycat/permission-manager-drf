from unittest.mock import PropertyMock

import pytest
from rest_framework import status

from tests.app.views import TestModelViewSet


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ('client_name', 'expected_permissions'),
    [
        ('admin_client', {'create': {'allow': True, 'messages': None}}),
        ('user_client', {'create': {'allow': False, 'messages': None}}),
    ],
)
def test_default_list_actions(request, client_name, expected_permissions):
    client = request.getfixturevalue(client_name)
    response = client.get(path='/model/')
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data['permissions'] == expected_permissions


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
