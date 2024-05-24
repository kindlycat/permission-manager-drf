from contextlib import suppress

from django.core.exceptions import ImproperlyConfigured

from permission_manager_drf.utils import get_permission_manager


class PermissionManagerPaginationMixin:
    """Mixin to add permission manager resolved permissions to pagination.

    This mixin integrates permission manager into the paginated response of a
    DRF pagination class.
    """

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate the queryset.

        This method overrides the default `paginate_queryset` to store the
        view for later use.

        Args:
            queryset: The queryset to paginate.
            request: The request object.
            view: The view object (optional).

        Returns:
            The paginated queryset.
        """
        self.view = view
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        """Get the paginated response.

        This method overrides the default `get_paginated_response` to add
        permission manager results to the response data.

        Args:
            data: The paginated data.

        Returns:
            The paginated response with added permission manager results.
        """
        result = super().get_paginated_response(data)

        with suppress(ImproperlyConfigured, AttributeError, TypeError):
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
