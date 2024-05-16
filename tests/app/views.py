from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from permission_manager_drf import ManagerPermission, PermissionField
from permission_manager_drf.fields import PermissionFieldChild
from tests.app.models import (
    TestChildModelPermissionManager,
    TestModel,
    TestModelStatus,
)
from tests.app.pagination import TestPagination


class TestModelSerializer(ModelSerializer):
    __test__ = False

    permissions = PermissionField(
        actions=('update', 'publish'),
        children=[
            PermissionFieldChild(
                name='child_model',
                manager=TestChildModelPermissionManager,
                actions=['create'],
            )
        ],
    )

    class Meta:
        model = TestModel
        fields = '__all__'


class TestModelViewSet(ModelViewSet):
    __test__ = False

    permission_classes = [IsAuthenticated, ManagerPermission]
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
    pagination_class = TestPagination

    @action(detail=False, methods=['get'])
    def custom_non_detail(self, request, **kwargs):
        return Response(
            data={'custom_non_detail': True}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'])
    def publish(self, request, **kwargs):
        instance = self.get_object()
        instance.status = TestModelStatus.PUBLISHED
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def without_action(self, request, **kwargs):
        self.action = None
        self.get_object()
        return Response(status=status.HTTP_200_OK)
