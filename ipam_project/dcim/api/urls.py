from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
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

urlpatterns = router.urls

app_name = 'dcim_api'
