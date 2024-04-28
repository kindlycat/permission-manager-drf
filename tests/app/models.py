from django.db import models
from django.db.models import TextChoices
from permission_manager import PermissionResult

from permission_manager_drf.managers import DRFPermissionManager


class TestModelStatus(TextChoices):
    __test__ = False

    DRAFT = 'draft'
    PUBLISHED = 'published'


class TestModelPermissionManager(DRFPermissionManager):
    __test__ = False
    instance: 'TestModel'

    def has_create_permission(self) -> bool:
        return self.user.is_staff

    def has_update_permission(self) -> bool:
        return self.user.is_staff

    def has_delete_permission(self) -> bool:
        return self.user.is_staff

    def has_publish_permission(self) -> bool:
        if not self.user.is_staff:
            return False

        return PermissionResult(
            message='Already published',
            value=self.instance.status == TestModelStatus.DRAFT,
        )

    def has_view_permission(self) -> bool:
        return (
            self.user.is_staff
            or self.instance.status == TestModelStatus.PUBLISHED
        )

    def has_list_permission(self) -> bool:
        return True

    def has_custom_non_detail_permission(self) -> bool:
        return PermissionResult(
            message='Only staff can do it',
            value=self.user.is_staff,
        )


class TestModel(models.Model):
    __test__ = False

    title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=TestModelStatus.choices,
        default=TestModelStatus.DRAFT,
    )

    permission_manager = TestModelPermissionManager

    class Meta:
        verbose_name = 'Test model'
        ordering = ['pk']

    def __str__(self) -> str:
        return self.title


class TestChildModelPermissionManager(DRFPermissionManager):
    __test__ = False

    def has_create_permission(self) -> bool:
        return PermissionResult(
            message='Parent is not editable',
            value=self.parent_permission_manager.has_update_permission(),
        )


class TestChildModel(models.Model):
    __test__ = False

    title = models.CharField(max_length=100)
    test_model = models.ForeignKey(TestModel, on_delete=models.CASCADE)

    permission_manager = TestChildModelPermissionManager

    class Meta:
        verbose_name = 'Test child model'
        ordering = ['pk']

    def __str__(self) -> str:
        return self.title
