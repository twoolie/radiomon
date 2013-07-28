
from django.db.models import (Model,
	ForeignKey, TextField, CharField, DateTimeField, PositiveIntegerField)

class TransmissionInfo(Model):

	datetime = CharField(max_length=16, unique=True)
	comments = TextField()
	category = CharField(max_length=16, default="None")
	lastedit = CharField(max_length=16)
	txinfo   = CharField(max_length=16)

	class Meta:
		db_table = 'transmissioninfo'

class Channel(Model):

	# Channel Metadata
	title      = CharField(max_length=100)
	short_name = CharField(max_length=20)
	frequency  = PositiveIntegerField(
		help_text="Frequency of transmission in Khz")

	# Recording Settings
	threshold       = PositiveIntegerField()
	chop_from_start = PositiveIntegerField()
	initial_timeout = PositiveIntegerField()

	class Meta:
		ordering = ['frequency']

class Transmission(Model):

	# Accounting
	channel    = ForeignKey(Channel)
	start_time = DateTimeField()
	end_time   = DateTimeField()

	# User Categorisation
	editor     = ForeignKey('auth.User', null=True)
	last_edit  = DateTimeField(auto_now=True)
	category   = CharField(max_length=50)
	comments   = TextField()
	segments   = TextField(editable=False,
		help_text="Legacy Segment Data")

	class Meta:
		ordering = ['start_time']

class Segment(Model):

	# Accounting
	transmission   = ForeignKey(Channel)
	start_timecode = PositiveIntegerField()
	end_timecode   = PositiveIntegerField()

	class Meta:
		ordering = ['start_timecode']
		unique_together = [('transmission','start_timecode'),
		                   ('transmission', 'end_timecode')]
