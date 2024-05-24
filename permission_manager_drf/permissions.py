from typing import TYPE_CHECKING, ClassVar

from rest_framework.permissions import BasePermission

from permission_manager_drf.utils import get_permission_manager


if TYPE_CHECKING:
    from django.db.models import Model
    from rest_framework.request import Request
    from rest_framework.viewsets import GenericViewSet


class ManagerPermission(BasePermission):
    """DRF Permission class for a permission manager.

    This class integrates with a permission manager to handle permissions
    for DRF views and objects.

    Attributes:
        default_detail_actions (ClassVar[tuple]): Default actions considered
            as detail actions.
    """

    default_detail_actions: ClassVar[tuple] = ('retrieve', 'destroy', 'update')

    def is_detail(self, view: 'GenericViewSet', action_name: str) -> bool:
        """Check if the action is a detail action.

        Args:
            view (GenericViewSet): The view being accessed.
            action_name (str): The name of the action.

        Returns:
            bool: True if the action is a detail action, False otherwise.
        """
        if action_name in self.default_detail_actions:
            return True

        action = getattr(view, action_name)
        return getattr(action, 'detail', False)

    def _has_perm(self, view: 'GenericViewSet', obj: 'Model' = None) -> bool:
        """Check if the permission is granted for the action.

        Args:
            view (GenericViewSet): The view being accessed.
            obj (Model, optional): The object being accessed.

        Returns:
            bool: True if the permission is granted, False otherwise.
        """
        action_name = view.action

        # Let DRF decide what to do if view hasn't action
        if not action_name:
            return True

        # Resolve partial_update action like update action
        if action_name == 'partial_update':
            action_name = 'update'

        if not obj and self.is_detail(view=view, action_name=action_name):
            return True

        manager = get_permission_manager(view=view, instance=obj)
        return manager.has_permission(action_name)

    def has_permission(
        self,
        request: 'Request',
        view: 'GenericViewSet',
    ) -> bool:
        """Check if the request has permission to access the view.

        Args:
            request (Request): The request being made.
            view (GenericViewSet): The view being accessed.

        Returns:
            bool: True if the request has permission, False otherwise.
        """
        return self._has_perm(view=view)

    def has_object_permission(
        self,
        request: 'Request',
        view: 'GenericViewSet',
        obj: 'Model',
    ) -> bool:
        """Check if the request has permission to access the object.

        Args:
            request (Request): The request being made.
            view (GenericViewSet): The view being accessed.
            obj (Model): The object being accessed.

        Returns:
            bool: True if the request has permission, False otherwise.
        """
        return self._has_perm(view=view, obj=obj)
