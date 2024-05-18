from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from permission_manager import BasePermissionManager
from permission_manager.types import ResolveWithMessageResult
from rest_framework.fields import Field, SkipField

from permission_manager_drf.utils import get_permission_manager


@dataclass(kw_only=True)
class PermissionFieldChild:
    """Dataclass for defining 'children' attribute in PermissionField.

    Attributes:
        name (str): The name of the child permission.
        manager (type[BasePermissionManager]): The permission manager class
            for the child field.
        actions (Iterable[str]): The list of actions for the child permission
            field.
    """

    name: str
    manager: type[BasePermissionManager]
    actions: Iterable[str]


class PermissionField(Field):
    """DRF field for representing permissions.

    This field is used to represent permissions in a Django Rest Framework
    serializer.

    Attributes:
        actions (Iterable[str]): The actions to be checked for permissions.
        children (Iterable[PermissionFieldChild] | None): The child permissions
            Defaults to None.
        with_messages (bool): Whether to include messages in the permission
            result. Defaults to True.
    """

    def __init__(
        self,
        *,
        actions: Iterable[str],
        children: Iterable[PermissionFieldChild] | None = None,
        with_messages: bool = True,
        **kwargs,
    ) -> None:
        """Initialize the PermissionField.

        Args:
            actions (Iterable[str]): The actions to be checked for permissions.
            children (Iterable[PermissionFieldChild] | None): The child
                permissions. Defaults to None.
            with_messages (bool): Whether to include messages in the permission
                result. Defaults to True.
            **kwargs: Additional keyword arguments for the field.
        """
        self.actions = actions
        self.children = children or ()
        self.with_messages = with_messages

        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super().__init__(**kwargs)

    def get_attribute(self, instance: Any) -> Any:
        """Get the attribute from the instance.

        This method ensures that the context contains both 'request' and 'view'
        before retrieving the attribute.

        Args:
            instance: The instance from which to retrieve the attribute.

        Raises:
            SkipField: If the context does not contain 'request' and 'view'.
        """
        if not {'request', 'view'} <= set(self.context):
            raise SkipField
        return super().get_attribute(instance)

    def to_representation(
        self,
        value: Any,
    ) -> dict[str, bool] | dict[str, ResolveWithMessageResult]:
        """Convert the field value to a dictionary representation.

        This method resolves the permissions for the specified actions and
        includes the results from any child permission fields.

        Args:
            value: The instance.

        Returns:
            dict: The dictionary representation of the permissions.
        """
        view = self.context['view']
        manager = get_permission_manager(
            view=view,
            instance=value,
            cache=True,
        )
        result = manager.resolve(
            actions=self.actions, with_messages=self.with_messages
        )

        for child in self.children:
            result[child.name] = child.manager(
                user=view.request.user,
                parent=value,
                parent_permission_manager=manager,
                cache=True,
            ).resolve(actions=child.actions, with_messages=self.with_messages)

        return result
