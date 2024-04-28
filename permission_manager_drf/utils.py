from django.core.exceptions import ImproperlyConfigured
from permission_manager import BasePermissionManager


def get_permission_manager(
    *,
    view,
    instance=None,
    cache: bool = False,
) -> BasePermissionManager:
    """Get a permission manager instance from a view.

    :param view: drf view
    :param instance: model instance
    :param cache: set permission manager cache
    :return: permission_manager instance.
    """
    if view_manager_class := getattr(view, 'get_permission_manager', None):
        manager_class = view_manager_class()
    elif view_manager_class := getattr(view, 'permission_manager', None):
        manager_class = view_manager_class
    elif (queryset := getattr(view, 'queryset', None)) is not None:
        manager_class = get_permission_manager_class_for_model(queryset.model)
    elif model := getattr(view, 'model', None):
        manager_class = get_permission_manager_class_for_model(model)
    else:
        msg = (
            "You must define the 'get_permission_manager' method, "
            "or the 'permission_manager' attribute, or the 'model' "
            'attribute in the view.'
        )
        raise ImproperlyConfigured(msg)

    return manager_class(
        user=view.request.user,
        instance=instance,
        cache=cache,
        **getattr(view, 'get_permission_manager_context', {}),
    )


def get_permission_manager_class_for_model(
    model,
) -> type[BasePermissionManager]:
    """Get a permission manager class from a model.

    :param model: django model
    :return: permission manager class.
    """
    return model.permission_manager
