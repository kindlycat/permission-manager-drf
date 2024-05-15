===============
Getting Started
===============

Permission-manager-drf provides a simple way to manage permissions using
`permission-manager`_.
Say we have a ``News`` model and we want to declare permissions for it.

The model
---------

Let's start with our model:

..  code-block:: Python

    from django.db import models


    class NewsStatus(models.TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'


    class News(models.Model):
        title = models.CharField(max_length=255)
        status = models.CharField(max_length=10, choices=NewsStatus.choices)
        content = models.TextField()


The permission manager
----------------------

Now create a ``DRFPermissionManager`` for this model:

..  code-block:: Python

    import permission_manager_drf import DRFPermissionManager

    class NewsPermissionManager(DRFPermissionManager):
        def has_create_permission(self) -> bool:
            return self.user.is_staff

        def has_update_permission(self) -> bool:
            return self.user.is_staff

        def has_delete_permission(self) -> bool:
            self.has_update_permission()

        def has_list_permission(self) -> bool:
            return True

        def has_view_permission(self) -> bool:
            return (
                self.user.is_staff
                or self.instance.status == TestModelStatus.PUBLISHED
            )

        def has_publish_permission(self) -> bool:
            return (
                self.has_update_permission()
                and self.instance.status == TestModelStatus.DRAFT
            )

So, we have just described each action we can perform with our model using
methods. ``DRFPermissionManager`` provides standard permissions for DRF, such
as ``create``, ``update``, ``delete``, ``list``, ``view``, and they ``False``
by default."

.. note::

    ``delete`` and ``view`` actions are aliases for ``destroy`` and
    ``retrieve`` in DRF.


Add it to the model
~~~~~~~~~~~~~~~~~~~

To associate permission manager and our model we need to add an attribute to
the model:

..  code-block:: Python

    class News(models.Model):
        ...
        permission_manager = NewsPermissionManager


The view
--------
Now we need to write a view:

..  code-block:: Python

    from rest_framework.decorators import action
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.viewsets import ModelViewSet

    from permission_manager_drf import ManagerPermission


    class NewsViewSet(ModelViewSet):
        permission_classes = [IsAuthenticated, ManagerPermission]
        queryset = News.objects.all()

        @action(detail=True, methods=['patch'])
        def publish(self, request, **kwargs):
            instance = self.get_object()
            instance.status = TestModelStatus.PUBLISHED
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


That's all, now our permission manager will check all the actions in the view.

.. note::

    By default, ``permission_manager_drf`` looks for a permission manager in
    this order:

        * ``get_permission_manager`` method in the view.
        * ``permission_manager`` attribute in the view.
        * ``permission_manager`` attribute in the model from the ``queryset`` attribute in the view.
        * ``permission_manager`` attribute in the model from the ``model`` attribute in the view.

    if you want to change the ``permission_manager`` attribute in model, you can
    define the ``PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER`` setting.


.. _permission-manager: https://github.com/kindlycat/permission-manager
