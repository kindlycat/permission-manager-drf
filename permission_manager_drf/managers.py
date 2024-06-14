from permission_manager import PermissionManager
from permission_manager.decorators import alias
from permission_manager.manager import BasePermissionMeta


class DRFAliasMeta(type):
    """Metaclass that adds aliases for permissions.

    This metaclass decorates permission methods with aliases corresponding
    to Django Rest Framework (DRF) action names.
    """

    def __new__(cls, *args, **kwargs) -> type:
        """Create a new class instance and apply decorations.

        Returns:
            type: The newly created class with decorated methods.
        """
        new_cls = super().__new__(cls, *args, **kwargs)
        new_cls.decorate()
        return new_cls

    def decorate(cls) -> None:
        """Decorate permission methods with DRF action aliases.

        This method adds aliases for 'retrieve' to `has_view_permission` and
        for 'destroy' to `has_delete_permission`.
        """
        cls.has_view_permission = alias('retrieve')(cls.has_view_permission)
        cls.has_delete_permission = alias('destroy')(cls.has_delete_permission)


class DRFPermissionManagerMeta(BasePermissionMeta, DRFAliasMeta):
    """Metaclass combining BasePermissionMeta and DRFAliasMeta.

    This metaclass inherits functionality from both BasePermissionMeta and
    DRFAliasMeta to provide a comprehensive metaclass for DRF permission
    management.
    """


class DRFPermissionManager(
    PermissionManager,
    metaclass=DRFPermissionManagerMeta,
):
    """Base DRF permission manager class.

    This class defines the base permissions for various DRF actions. Each
    method returns a boolean indicating whether the permission is granted.
    """

    def has_create_permission(self) -> bool:
        """Check if create permission is granted.

        Returns:
            bool: False by default.
        """
        return False

    def has_update_permission(self) -> bool:
        """Check if update permission is granted.

        Returns:
            bool: False by default.
        """
        return False

    def has_view_permission(self) -> bool:
        """Check if view permission is granted.

        Returns:
            bool: False by default.
        """
        return False

    def has_delete_permission(self) -> bool:
        """Check if delete permission is granted.

        Returns:
            bool: False by default.
        """
        return False

    def has_list_permission(self) -> bool:
        """Check if list permission is granted.

        Returns:
            bool: False by default.
        """
        return False
