from django.forms import widgets
from rest_framework import serializers
from api_v_1.models import API_Device, LANGUAGE_CHOICES, STYLE_CHOICES


class API_DeviceSerializer(serializers.Serializer):
	pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
	title = serializers.CharField(required=False,
                                  max_length=100)
	model = serializers.CharField(required=False, max_length=50)
	imei = serializers.CharField(required=False, max_length=18)
	phone_number = serializers.CharField(required=False, max_length=32)
	mac = serializers.CharField(required=False, max_length=20)
	usbidcode = serializers.CharField(required=False, max_length=30)
	latitude = serializers.CharField(required=False, max_length=50)
	longitude = serializers.CharField(required=False, max_length=50)
	height = serializers.CharField(required=False, max_length=50)
	cell_id = serializers.BooleanField(required=False)
	ip_info = serializers.CharField(required=False, max_length=128)
	wifi_info = serializers.CharField(required=False, max_length=512)
	battery_info = serializers.CharField(required=False, max_length=128)
	webcam_picture = serializers.CharField(required=False, max_length=128)
	code = serializers.CharField(widget=widgets.Textarea, max_length=100000)
	style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
	
	def restore_object(self, attrs, instance=None):
	
		if instance:
			instance.title = attrs.get('title', instance.title)
			model = attrs.get('model', instance.code)
			imei = attrs.get('imei', instance.imei)
			phone_number = attrs.get('phone_number', instance.phone_number)
			mac = attrs.get('mac', instance.mac)
			usbidcode = attrs.get('usbidcode', instance.usbidcode)
			latitude = attrs.get('latitude', instance.latitude)
			longitude = attrs.get('longitude', instance.longitude)
			height = attrs.get('height', instance.height)
			cell_id = attrs.get('cell_id', instance.cell_id)
			ip_info = attrs.get('ip_info', instance.ip_info)
			wifi_info = attrs.get('wifi_info', instance.wifi_info)
			battery_info = attrs.get('battery_info', instance.battery_info)
			webcam_picture = attrs.get('webcam_picture', instance.webcam_picture)
			instance.code = attrs.get('code', instance.code)
			instance.style = attrs.get('style', instance.style)
			return instance
			
		return API_Device(**attrs)
		
		
class API_DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = API_Device
        fields = ('id', 'title', 'model', 'imei', 'model', 'phone_number', 'mac', 'usbidcode', 'latitude', 'longitude', 'height', 'cell_id', 'ip_info', 'wifi_info', 'battery_info', 'code', 'style')