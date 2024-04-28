from rest_framework.pagination import PageNumberPagination

from permission_manager_drf.pagination import PermissionManagerPaginationMixin


class TestPagination(PermissionManagerPaginationMixin, PageNumberPagination):
    page_size = 10
