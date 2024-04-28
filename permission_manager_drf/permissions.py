from typing import ClassVar

from django.db.models import Model
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from permission_manager_drf.utils import get_permission_manager


class ManagerPermission(BasePermission):
    """DRF Permission class for a permission manager."""

    default_detail_actions: ClassVar[tuple] = ('retrieve', 'destroy', 'update')

    def is_detail(self, view: GenericViewSet, action_name: str) -> bool:
        """Check if action is detail."""
        if action_name in self.default_detail_actions:
            return True

        action = getattr(view, action_name)
        return getattr(action, 'detail', False)

    def _has_perm(self, view: GenericViewSet, obj: Model = None) -> bool:
        action_name = view.action

        # Let drf decide what to do if view hasn't action
        if not action_name:
            return True

        # Resolve partial_update action like update action
        if action_name == 'partial_update':
            action_name = 'update'

        if not obj and self.is_detail(view=view, action_name=action_name):
            return True

        manager = get_permission_manager(view=view, instance=obj)
        return manager.has_permission(action_name)

    def has_permission(self, request: Request, view: GenericViewSet) -> bool:
        return self._has_perm(view=view)

    def has_object_permission(
        self,
        request: Request,
        view: GenericViewSet,
        obj: Model,
    ) -> bool:
        return self._has_perm(view=view, obj=obj)
