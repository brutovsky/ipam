from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'dcim-api'
urlpatterns = [
    path('regions/', views.RegionList.as_view()),
    path('regions/<int:pk>/', views.RegionDetail.as_view()),
    path('sites/', views.SiteList.as_view()),
    path('sites/<int:pk>/', views.SiteDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
