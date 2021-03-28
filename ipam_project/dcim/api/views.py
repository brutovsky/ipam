from .serializers import RegionSerializer, SiteSerializer
from dcim.models.site import Region, Site

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#
# Region
#

class RegionList(APIView):
    queryset = Region.objects.all()
    """
    List all regions.
    """
    def get(self, request, format=None):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionDetail(APIView):
    queryset = Region.objects.all()
    """
    Retrieve, update or delete a region.
    """
    def get_object(seld,pk):
        try:
            return Region.objects.get(pk=pk)
        except Region.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        region = self.get_object(pk)
        serializer = RegionSerializer(region)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        region = self.get_object(pk)
        serializer = RegionSerializer(region, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        region = self.get_object(pk)
        print(region)
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# Site
#

class SiteList(APIView):
    queryset = Site.objects.all()
    """
    List all sites.
    """
    def get(self, request, format=None):
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteDetail(APIView):
    queryset = Site.objects.all()
    """
    Retrieve, update or delete a site.
    """
    def get_object(seld,pk):
        try:
            return Site.objects.get(pk=pk)
        except Site.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        site = self.get_object(pk)
        serializer = SiteSerializer(site)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        site = self.get_object(pk)
        serializer = SiteSerializer(site, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        site = self.get_object(pk)
        print(site)
        site.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
