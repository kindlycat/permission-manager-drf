from dataclasses import dataclass
from functools import partial
from importlib import reload
from typing import NamedTuple

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from permission_manager import BasePermissionManager

import permission_manager_drf.settings
from permission_manager_drf.managers import DRFPermissionManager
from permission_manager_drf.utils import get_permission_manager
from tests.app.models import (
    TestModel,
    TestModelPermissionManager,
)


def custom_permission_manager_drf_for_model_getter(model):
    return model.test_permission_manager


@pytest.mark.django_db()
def test_get_permission_manager_class_for_model():
    assert (
        permission_manager_drf.settings.permission_manager_getter(TestModel)
        is TestModel.permission_manager
    )


@pytest.mark.django_db()
@override_settings(
    PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER=(
        'tests.test_utils.custom_permission_manager_drf_for_model_getter'
    )
)
def test_custom_get_permission_manager_class_for_model():
    reload(permission_manager_drf.settings)
    TestModel.test_permission_manager = DRFPermissionManager
    assert (
        permission_manager_drf.settings.permission_manager_getter(TestModel)
        is TestModel.test_permission_manager
    )


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'attributes',
    [
        {
            'get_permission_manager': lambda: TestModelPermissionManager,
            'permission_manager': None,
            'queryset': None,
            'model': None,
        },
        {
            'get_permission_manager': None,
            'permission_manager': TestModelPermissionManager,
            'queryset': None,
            'model': None,
        },
        {
            'get_permission_manager': None,
            'permission_manager': None,
            'queryset': TestModel.objects.all(),
            'model': None,
        },
        {
            'get_permission_manager': None,
            'permission_manager': None,
            'queryset': None,
            'model': TestModel,
        },
    ],
)
def test_get_permission_manager_positive(attributes):
    class Request(NamedTuple):
        user = None

    class View:
        request = Request()

    for k, v in attributes.items():
        setattr(View, k, v)

    assert isinstance(
        get_permission_manager(view=View), TestModelPermissionManager
    )


@pytest.mark.django_db()
def test_get_permission_manager_negative():
    class Request(NamedTuple):
        user = None

    class View:
        request = Request()

    with pytest.raises(ImproperlyConfigured):
        get_permission_manager(view=View)


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ('attributes', 'expected_key'),
    [
        (
            {
                'get_permission_manager': TestModelPermissionManager.create(
                    'MethodGetPermissionManagerClass'
                ),
                'permission_manager': TestModelPermissionManager.create(
                    'AttributePermissionManagerClass'
                ),
                'queryset': TestModelPermissionManager.create('QuerysetClass'),
                'model': TestModelPermissionManager.create('ModelClass'),
            },
            'get_permission_manager',
        ),
        (
            {
                'get_permission_manager': None,
                'permission_manager': TestModelPermissionManager.create(
                    'AttributePermissionManagerClass'
                ),
                'queryset': TestModelPermissionManager.create('QuerysetClass'),
                'model': TestModelPermissionManager.create('ModelClass'),
            },
            'permission_manager',
        ),
        (
            {
                'get_permission_manager': None,
                'permission_manager': None,
                'queryset': TestModelPermissionManager.create('QuerysetClass'),
                'model': TestModelPermissionManager.create('ModelClass'),
            },
            'queryset',
        ),
        (
            {
                'get_permission_manager': None,
                'permission_manager': None,
                'queryset': None,
                'model': TestModelPermissionManager.create('ModelClass'),
            },
            'model',
        ),
    ],
)
def test_get_permission_manager_multiple_attributes(attributes, expected_key):
    @dataclass
    class Model:
        permission_manager: BasePermissionManager = None

    @dataclass
    class QuerySet:
        model: Model | None = None

    class Request(NamedTuple):
        user = None

    class View:
        request = Request()

    for k, v in attributes.items():
        match k:
            case 'get_permission_manager' if v:
                View.get_permission_manager = partial(
                    lambda value: value, value=v
                )
            case 'permission_manager' if v:
                View.permission_manager = v
            case 'queryset' if v:
                View.queryset = QuerySet(model=Model(permission_manager=v))
            case 'model' if v:
                View.model = Model(permission_manager=v)
    assert isinstance(
        get_permission_manager(view=View),
        attributes[expected_key],
    )
