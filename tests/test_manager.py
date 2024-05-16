import pytest

from permission_manager_drf import DRFPermissionManager


@pytest.mark.parametrize(
    'action', ['create', 'update', 'delete', 'view', 'list']
)
def test_drf_permission_manager(action):
    manager = DRFPermissionManager()

    assert manager.has_permission(action) is False
