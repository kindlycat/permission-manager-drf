from rest_framework.routers import SimpleRouter

from tests.app.views import TestModelViewSet


router = SimpleRouter()
router.register('model', TestModelViewSet)


urlpatterns = router.urls
