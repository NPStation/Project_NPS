from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class API_Device(models.Model):
	#owner = models.ForeignKey('auth.User', related_name='API_Devices')
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=100, blank=True, default='')
	model = models.CharField(max_length=50, blank=True, default='')
	imei = models.CharField(max_length=18, blank=True, default='')
	phone_number = models.CharField(max_length=32, blank=True, default='')
	mac = models.CharField(max_length=20, blank=True, default='')
	usbidcode = models.CharField(max_length=30, blank=True, default='')
	latitude = models.CharField(max_length=50, blank=True, default='')
	longitude = models.CharField(max_length=50, blank=True, default='')
	height = models.CharField(max_length=50, blank=True, default='')
	cell_id = models.BooleanField(default=False)
	ip_info = models.CharField(max_length=128, blank=True, default='')
	wifi_info = models.CharField(max_length=512, blank=True, default='')
	battery_info = models.CharField(max_length=128, blank=True, default='')
	webcam_picture = models.CharField(max_length=128, blank=True, default='')
	code = models.TextField()
	style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

	class Meta:
		ordering = ('created',)