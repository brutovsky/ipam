from . import views
from rest_framework import routers


class IpamApi(routers.APIRootView):
    """
    IPAM App api root
    """
    pass


class DocumentedRouter(routers.DefaultRouter):
    APIRootView = IpamApi


router = DocumentedRouter()

router.register('ip_role', views.IPRoleViewSet, basename='ip_role')
router.register('ip_address', views.IPAddressViewSet, basename='ip_address')
router.register('ip_prefix', views.IPPrefixViewSet, basename='ip_prefix')

router.register('vlan_role', views.VLANRoleViewSet, basename='vlan_role')
router.register('vlan_group', views.VLANGroupViewSet, basename='vlan_group')
router.register('vlan', views.VLANViewSet, basename='vlan')

router.register('service', views.ServiceViewSet, basename='service')

urlpatterns = router.urls

app_name = 'ipam_api'
