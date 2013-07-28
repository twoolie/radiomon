
from django.contrib.admin import ModelAdmin

from .models import Channel, Transmission

class ChannelAdmin(ModelAdmin):
	list_display = ("title", "frequency")


class TransmissionAdmin(ModelAdmin):
	list_display = ("id", "start_time", "end_time")
