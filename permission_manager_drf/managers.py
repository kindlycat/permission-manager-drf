from permission_manager import PermissionManager
from permission_manager.decorators import alias
from permission_manager.manager import BasePermissionMeta


class DRFAliasMeta(type):
    """Metaclass that adds alias for drf actions."""

    def __new__(cls, *args, **kwargs) -> type:
        new_cls = super().__new__(cls, *args, **kwargs)
        new_cls.decorate()
        return new_cls

    def decorate(cls) -> None:
        cls.has_view_permission = alias(['retrieve'])(cls.has_view_permission)
        cls.has_delete_permission = alias(['destroy'])(
            cls.has_delete_permission
        )


class DRFPermissionManagerMeta(BasePermissionMeta, DRFAliasMeta): ...


class DRFPermissionManager(
    PermissionManager,
    metaclass=DRFPermissionManagerMeta,
):
    """Base DRF permission manager class."""

    def has_create_permission(self) -> bool:
        return False

    def has_update_permission(self) -> bool:
        return False

    def has_view_permission(self) -> bool:
        return False

    def has_delete_permission(self) -> bool:
        return False

    def has_list_permission(self) -> bool:
        return False
