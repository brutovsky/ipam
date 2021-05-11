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
router.register('locations', views.LocationViewSet)

router.register('rack_groups', views.RackGroupViewSet, basename='rack_group')
router.register('rack_roles', views.RackRoleViewSet, basename='rack_role')
router.register('racks', views.RackViewSet, basename='rack')

router.register('manufacturer', views.ManufacturerViewSet, basename='manufacturer')
router.register('platform', views.PlatformViewSet, basename='platform')
router.register('device_type', views.DeviceTypeViewSet, basename='device_type')
router.register('device_role', views.DeviceRoleViewSet, basename='device_role')
router.register('device', views.DeviceViewSet, basename='device')

urlpatterns = router.urls

app_name = 'dcim_api'
