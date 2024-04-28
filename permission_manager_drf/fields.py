from collections.abc import Iterable
from dataclasses import dataclass

from permission_manager import BasePermissionManager
from rest_framework.fields import Field, SkipField

from permission_manager_drf.utils import get_permission_manager


@dataclass(kw_only=True)
class PermissionFieldChild:
    """Dataclass for defining 'children' attribute in PermissionField."""

    name: str
    manager: type[BasePermissionManager]
    actions: Iterable[str]


class PermissionField(Field):
    """DRF field for representing permissions."""

    def __init__(
        self,
        *,
        actions: Iterable,
        children: Iterable[PermissionFieldChild] | None = None,
        with_messages: bool = True,
        **kwargs,
    ) -> None:
        self.actions = actions
        self.children = children or ()
        self.with_messages = with_messages

        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super().__init__(**kwargs)

    def get_attribute(self, instance) -> None:
        if not {'request', 'view'} <= set(self.context):
            raise SkipField
        return super().get_attribute(instance)

    def to_representation(self, value) -> dict:
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
