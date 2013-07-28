
import os, sys, time, struct, datetime
import subprocess, traceback
import pyaudio, wave

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...models import Channel, Transmission, Segment

import logging; log = logging.getLogger(__module__)

rectimeout = 0
recdata = ""
starttime = 0
wf = None
filename = None
df = None
dfcont = ""
filetime = 0
datecode = None
timecode = None

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option('--channel', dest='channel',
			help='The short name of the channel to record'),
		)
	can_import_settings = True

	def handle(self, channel, **options):
		try:
			channel = Channel.objects.get(short_name=channel)
		except Channel.DoesNotExist:
			print "Channel with this shortcode does not exist!"
			sys.exit(-1)

		self.p = pyaudio.PyAudio()
		try:
			self.do_record(channel)
		finally:
			self.p.terminate()

	def openwav(self,filename):
		wf = wave.open(filename,'wb')
		wf.setnchannels(1)
		wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
		wf.setframerate(11025)
		return wf

	def do_record(self, channel):
		"""  NEEDS MASSIVE REFACTORING """
		stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=11025, input=True, frames_per_buffer=256)
		try:
			while True:
				try:
					data = stream.read(256)
				except IOError:
					log.warning("Frame dropped")
					continue
				d = struct.unpack("256h",data)
				vol = max(d)
				if vol > channel.threshold:
					#print "vol: %i" % vol
					if rectimeout == 0:
						recdata = ""
						log.info("Started recording at %s", time.strftime("%H:%M:%S"))
						starttime = datetime.datetime.now()
						if time.time() - starttime > (60*5):
							filetime = 0
							if wf:
								log.info("Closing File %s", filename)
								endtime = datetime.datetime.now()
								wf.close()
								subprocess.Popen(["/usr/bin/oggenc","-b","24",filename], stdout=sys.stdout)
								try:
									#cursor.execute("INSERT INTO transmissioninfo (datetime,comments,category,lastedit,txinfo) VALUES (%(datetime)s, '', 'none', 'initial', %(txinfo)s)",
									#			{'datetime': datecode + timecode, 'txinfo': dfcont})
									Transmission.objects.create(channel=channel,
										start_time = starttime, end_time = endtime)
									# TODO: Add Segments
								except Exception:
									log.exception("Could Not create Transmission")
							if df: df.close()
							datecode = time.strftime("%Y%m%d")
							timecode = time.strftime("%H%M")
							filename = "output/%s/rec%s.wav" % (datecode,timecode)
							dfilename = "output/%s/rec%s.txt" % (datecode,timecode)
							if not os.path.exists("output/%s/" % datecode):
								os.mkdir("output/"+datecode)
							wf = self.openwav(filename)
							df = open(dfilename,'w')
							dfcont = ""
							log.info("Opening new file: %s", filename)
						starttime = time.time()
					rectimeout = channel.initialtimeout
				if rectimeout > 0:
					rectimeout -= 1
					recdata += data
					if rectimeout == 0:
						if len(recdata) > channel.chopfromstart*2:
							nowtime = time.strftime("%H:%M:%S")
							reclen = time.time() - starttime
							log.info("Stopped recording at %s - %.2f seconds recorded", nowtime, reclen)
							frames = recdata[channel.chopfromstart*2:]
							wf.writeframes(frames)
							dfline = ("%f," % filetime)
							writelen = float(len(frames))/float(11025*2)
							filetime += writelen
							dfline += "%f,%f,%s\n" % (filetime,writelen,nowtime)
							df.write(dfline)
							dfcont += dfline
							df.flush()

		except KeyboardInterrupt:
			print "Stopping and closing file"
			wf.close()
			if filename:
				subprocess.Popen(["/usr/bin/oggenc","-b","24",filename], stdout=sys.stdout)
				#cursor.execute("INSERT INTO transmissioninfo (datetime,comments,category,lastedit,txinfo) VALUES (%(datetime)s, '', 'none', 'initial', %(txinfo)s)",
				#								{'datetime': datecode + timecode, 'txinfo': dfcont})
				Transmission.objects.create(channel=channel,
					start_time = starttime, end_time = endtime)
			df.close()
