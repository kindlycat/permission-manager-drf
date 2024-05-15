==========
Pagination
==========

This package provides a pagination mixin that adds the ability to retrieve
permissions in a list view.

.. code-block:: Python

    from permission_manager_drf.pagination import PermissionManagerPaginationMixin

    # Create pagination class with mixin
    class Pagination(PermissionManagerPaginationMixin, PageNumberPagination):
        page_size = 10


    # ViewSet
    class NewsViewSet(ModelViewSet):
        pagination_class = Pagination



Example output:

.. code-block:: JSON

    {
      "count": 0,
      "next": null,
      "previous": null,
      "results": [],
      "permissions": {
        "create": {
          "allow": true,
          "messages": null
        },
      }
    }

You can define which permissions should be serialized by adding the
``permission_manager_list_actions`` attribute to the view:

.. code-block:: Python

    class NewsViewSet(ModelViewSet):
        pagination_class = Pagination
        permission_manager_list_actions = ('create', 'custom_action')

.. code-block:: JSON

    {
      "count": 0,
      "next": null,
      "previous": null,
      "results": [],
      "permissions": {
        "create": {
          "allow": true,
          "messages": null
        },
        "custom_action": {
          "allow": true,
          "messages": null
        }
      }
    }
