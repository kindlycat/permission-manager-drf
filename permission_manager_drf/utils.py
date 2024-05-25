from contextlib import suppress
from typing import TYPE_CHECKING

from django.core.exceptions import ImproperlyConfigured


if TYPE_CHECKING:
    from django.db.models import Model
    from permission_manager import BasePermissionManager
    from permission_manager.types import ResolveWithMessageResult
    from rest_framework.viewsets import GenericViewSet


def get_permission_manager(
    *,
    view: 'GenericViewSet',
    instance: 'Model' = None,
    cache: bool = False,
) -> 'BasePermissionManager':
    """Get a permission manager instance from a view.

    Args:
        view: The DRF view from which to get the permission manager.
        instance: The model instance (optional).
        cache (bool): Whether to enable caching in the permission manager.

    Returns:
        BasePermissionManager: An instance of the permission manager.

    Raises:
        ImproperlyConfigured: If the view does not have a way to determine
            the permission manager.
    """
    manager_class = None
    if view_manager_class := getattr(view, 'get_permission_manager', None):
        manager_class = view_manager_class()
    elif view_manager_class := getattr(view, 'permission_manager', None):
        manager_class = view_manager_class
    elif (queryset := getattr(view, 'queryset', None)) is not None:
        manager_class = get_permission_manager_class_for_model(queryset.model)
    elif model := getattr(view, 'model', None):
        manager_class = get_permission_manager_class_for_model(model)

    if not manager_class:
        msg = (
            "You must define the 'get_permission_manager' method, "
            "or the 'permission_manager' attribute, or the 'model' "
            'attribute in the view.'
        )
        raise ImproperlyConfigured(msg)

    try:
        context = view.get_permission_manager_context()
    except AttributeError:
        context = {}

    return manager_class(
        user=view.request.user,
        instance=instance,
        cache=cache,
        **context,
    )


def get_permission_manager_class_for_model(
    model: 'Model',
) -> type['BasePermissionManager']:
    """Get a permission manager class for a given model.

    Args:
        model: The Django model for which to get the permission manager class.

    Returns:
        type[BasePermissionManager]: The permission manager class associated
            with the model.
    """
    return model.permission_manager


def get_list_permissions(
    view: 'GenericViewSet',
) -> list['ResolveWithMessageResult'] | None:
    """Get list permissions for a view.

    This function retrieves the permission manager for the given view and
    resolves the permissions for the specified actions, including messages
    if applicable.

    Args:
        view (GenericViewSet): The view for which to get the list permissions.

    Returns:
        list[ResolveWithMessageResult] | None: A list of resolved permissions
            with messages, or None if there was an error in getting the
            permission manager or resolving the permissions.
    """
    with suppress(ImproperlyConfigured, AttributeError, TypeError):
        manager = get_permission_manager(view=view, cache=True)
        actions = getattr(
            view,
            'permission_manager_list_actions',
            ['create'],
        )

        if manager and actions:
            return manager.resolve(actions=actions, with_messages=True)
