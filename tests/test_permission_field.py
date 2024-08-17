import pytest
from rest_framework import serializers

from permission_manager_drf import PermissionField
from tests.app.models import TestModel, TestModelStatus


@pytest.mark.django_db
def test_permission_field_by_admin(admin_client):
    instance = TestModel.objects.create(
        title='Test',
        status=TestModelStatus.PUBLISHED,
    )

    response = admin_client.get(path=f'/model/{instance.pk}/')

    assert response.json()['permissions'] == {
        'update': {
            'allow': True,
            'messages': None,
        },
        'publish': {
            'allow': False,
            'messages': ['Already published'],
        },
        'child_model': {
            'create': {
                'allow': True,
                'messages': None,
            },
        },
    }


@pytest.mark.django_db
def test_permission_field_by_user(user_client):
    instance = TestModel.objects.create(
        title='Test',
        status=TestModelStatus.PUBLISHED,
    )

    response = user_client.get(path=f'/model/{instance.pk}/')

    assert response.json()['permissions'] == {
        'update': {
            'allow': False,
            'messages': None,
        },
        'publish': {
            'allow': False,
            'messages': None,
        },
        'child_model': {
            'create': {
                'allow': False,
                'messages': ['Parent is not editable'],
            },
        },
    }


@pytest.mark.django_db
def test_permission_field_without_view_request_negative():
    instance = TestModel.objects.create(title='Test')

    class TestSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        permissions = PermissionField(actions=['update'])

    data = TestSerializer(instance=instance).data
    assert data == {'id': instance.pk}
