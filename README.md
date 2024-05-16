# Permission Manager for django rest framework

![example workflow](https://github.com/kindlycat/permission-manager-drf/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/kindlycat/permission-manager-drf/graph/badge.svg?token=5XAFJZS6A8)](https://codecov.io/gh/kindlycat/permission-manager-drf)

Use [permission_manager](https://github.com/kindlycat/permission-manager) for 
django rest framework.

Full documentation on [read the docs](https://permission-manager-drf.readthedocs.io/).

## Install

```bash
pip install permission-manager-drf
```

## Example
```python
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from permission_manager_drf import DRFPermissionManager, ManagerPermission
from permission_manager import PermissionResult


# Define permission manager
class SomeModelPermissionManager(DRFPermissionManager):
    def has_create_permission(self) -> bool:
        return self.user.is_staff

    def has_update_permission(self) -> bool:
        return self.user.is_staff

    def has_delete_permission(self) -> bool:
        return self.user.is_staff

    def has_view_permission(self) -> bool:
        return True

    def has_list_permission(self) -> bool:
        return True

    def has_custom_permission(self) -> bool:
        return PermissionResult(
            message="You can't do it",
            value=self.user.is_staff,
        )


# Define model with permission manager attribute
class SomeModel(models.Model):
    permission_manager = SomeModelPermissionManager
    ...


# ViewSet
class TestModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ManagerPermission]
    ...

    @action(detail=True)
    def custom(self, request, **kwargs):
        ...
```
That's all. Now every drf action will be checked by the permission manager.

Also, you can use the serializer field for retrieve permissions you need.

```python
from permission_manager_drf import PermissionField
from rest_framework.serializers import ModelSerializer

class SomeModelSerializer(ModelSerializer):
    permissions = PermissionField(actions=('view', 'custom'),)
    ...

"""
Example output:
{
    ...,
    'permissions': {
        'view': {
            'allow': True,
            'messages': None,
        },
        'custom': {
            'allow': False,
            'messages': ["You can't do it"],
        },
    }
}
"""
```
