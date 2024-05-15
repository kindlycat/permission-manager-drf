================
PermissionResult
================

The ``PermissionResult`` is a dataclass that helps you return messages why
certain permissions were denied. It's a part of ``permission_manager`` package.

Usage
~~~~~

.. code-block:: Python

    from permission_manager import PermissionResult
    from permission_manager_drf import DRFPermissionManager

    class NewsPermissionManager(DRFPermissionManager):
        def has_publish_permission() -> bool:
            return PermissionResult(
                message='Already published',
                value=self.instance.status != NewsStatus.PUBLISHED
            )

For more documentation, see the `permission manager docs`_.

.. _`permission manager docs`: https://permission-manager.readthedocs.io/en/latest/source/result.html