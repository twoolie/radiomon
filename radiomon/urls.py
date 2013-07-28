from django.conf.urls import patterns, include, url

from surlex.dj import surl
from .views import channel_index, transmission_index

urlpatterns = patterns('',
	surl(r"^chan:<channel_sn:s>$", channel_index, name="channel-index"),
	surl(r"^chan:<channel_sn:s>/xmit:<transmission_id:#>$", transmission_index, name="transmission-index")
)
