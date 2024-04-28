from permission_manager_drf.utils import get_permission_manager


class PermissionManagerPaginationMixin:
    """Add permission manager resolved results to pagination class."""

    def paginate_queryset(self, queryset, request, view=None):
        self.view = view
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        result = super().get_paginated_response(data)

        manager = get_permission_manager(view=self.view, cache=True)
        actions = getattr(
            self.view,
            'permission_manager_list_actions',
            ['create'],
        )
        if manager and actions:
            result.data['permissions'] = manager.resolve(
                actions=actions, with_messages=True
            )

        return result
