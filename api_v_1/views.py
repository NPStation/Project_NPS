# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.

def api_documentation(request):
    return render_to_response("api_v_1.html")
	

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api_v_1.models import *
from api_v_1.serializers import API_DeviceSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
		
		
# @csrf_exempt
# def api_v_1_list(request):
    # """
    # List all code api_v_1, or create a new snippet.
    # """
    # if request.method == 'GET':
        # api_v_1 = API_Device.objects.all()
        # serializer = API_DeviceSerializer(api_v_1, many=True)
        # return JSONResponse(serializer.data)

    # elif request.method == 'POST':
        # data = JSONParser().parse(request)
        # serializer = API_DeviceSerializer(data=data)
        # if serializer.is_valid():
            # serializer.save()
            # return JSONResponse(serializer.data, status=201)
        # return JSONResponse(serializer.errors, status=400)
		
		
# @csrf_exempt
# def api_v_1_detail(request, pk):
    # """
    # Retrieve, update or delete a code api_v_1.
    # """
    # try:
        # api_v_1 = API_Device.objects.get(pk=pk)
    # except API_Device.DoesNotExist:
        # return HttpResponse(status=404)

    # if request.method == 'GET':
        # serializer = API_DeviceSerializer(api_v_1)
        # return JSONResponse(serializer.data)

    # elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        # serializer = API_DeviceSerializer(api_v_1, data=data)
        # if serializer.is_valid():
            # serializer.save()
            # return JSONResponse(serializer.data)
        # return JSONResponse(serializer.errors, status=400)

    # elif request.method == 'DELETE':
        # api_v_1.delete()
        # return HttpResponse(status=204)
		
		
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_v_1.models import API_Device
from api_v_1.serializers import API_DeviceSerializer


@api_view(['GET', 'POST'])
def api_v_1_list(request, format=None):
    """
    List all api_v_1s, or create a new api_v_1.
    """
    if request.method == 'GET':
        api_v_1s = API_Device.objects.all()
        serializer = API_DeviceSerializer(api_v_1s, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = API_DeviceSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
@api_view(['GET', 'PUT', 'DELETE'])
def api_v_1_detail(request, pk, format=None):
    """
    Retrieve, update or delete a api_v_1 instance.
    """              
    try:
        api_v_1 = API_Device.objects.get(pk=pk)
    except API_Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = API_DeviceSerializer(api_v_1)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = API_DeviceSerializer(api_v_1, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        api_v_1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
		
from api_v_1.models import API_Device
from api_v_1.serializers import API_DeviceSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class API_DeviceList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        api_v_1s = API_Device.objects.all()
        serializer = API_DeviceSerializer(api_v_1s, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = API_DeviceSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
class API_DeviceDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return API_Device.objects.get(pk=pk)
        except API_Device.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        api_v_1 = self.get_object(pk)
        serializer = API_DeviceSerializer(api_v_1)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        api_v_1 = self.get_object(pk)
        serializer = API_DeviceSerializer(api_v_1, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        api_v_1 = self.get_object(pk)
        api_v_1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
		