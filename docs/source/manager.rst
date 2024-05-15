====================
DRFPermissionManager
====================

``Permission-manager-drf`` provides ``DRFPermissionManager``, which already
has default actions for rest framework, and by default, they are all set to
``False``.

It also contains aliases for ``retrieve`` (``view``) and ``destroy``
(``delete``) actions.

.. code-block:: Python

    from permission_manager_drf import DRFPermissionManager

    class ExamplePermissionManager(DRFPermissionManager):
        def has_create_permission(self) -> bool:
            return self.user.is_staff

        def has_update_permission(self) -> bool:
            return self.has_permission('create')

        def has_view_permission(self) -> bool:
            return True

        def has_delete_permission(self) -> bool:
            return False

        def has_list_permission(self) -> bool:
            return True


For more documentation, see the `permission manager docs`_.

.. _`permission manager docs`: https://permission-manager.readthedocs.io/en/latest/source/managers.html
