from . import views
from rest_framework import routers


class DcimApi(routers.APIRootView):
    """
    DCIM App api root
    """
    pass


class DocumentedRouter(routers.DefaultRouter):
    APIRootView = DcimApi


router = DocumentedRouter()

router.register('regions', views.RegionViewSet)
router.register('sites', views.SiteViewSet)

router.register('rack_groups', views.RackGroupViewSet, basename='rack_group')
router.register('rack_roles', views.RackRoleViewSet, basename='rack_role')
router.register('racks', views.RackViewSet, basename='rack')

urlpatterns = router.urls

app_name = 'dcim_api'
