# -*- coding: utf-8 -*-
import datetime, time
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        source_xmits = orm.TransmissionInfo.objects.all().iterator()

        default_channel = orm.Channel.objects.create(
            title='Default', short_name='default', frequency=0,
            threshold=600, chop_from_start=512, initial_timeout=25,)

        for transmission in source_xmits:
            txinfos = transmission.txinfo.split("\n")[:-1] # strip final empty line
            _,ftime,_,_ = txinfos[-1].split(",")
            start = datetime.datetime.strptime("%Y%m%%H%M", transmission.datetime)
            end = datetime.datetime.combine(
                 start.date(), datetime.datetime.strptime("%H%M",ftime).time())
            orm.Transmission.objects.create(
                channel = default_channel,
                category=transmission.category,
                start_time = start, end_time = end,
                segments = "|".join(txinfos)
            )
            #TODO: Create Segment Objects?


    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("There's no going back from here!")


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'radiomon.channel': {
            'Meta': {'ordering': "['frequency']", 'object_name': 'Channel'},
            'chop_from_start': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_timeout': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'threshold': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'radiomon.segment': {
            'Meta': {'ordering': "['start_timecode']", 'unique_together': "[('transmission', 'start_timecode'), ('transmission', 'end_timecode')]", 'object_name': 'Segment'},
            'end_timecode': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_timecode': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'transmission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radiomon.Channel']"})
        },
        u'radiomon.transmission': {
            'Meta': {'ordering': "['start_time']", 'object_name': 'Transmission'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['radiomon.Channel']"}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'segments': ('django.db.models.fields.TextField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'radiomon.transmissioninfo': {
            'Meta': {'object_name': 'TransmissionInfo', 'db_table': "'transmissioninfo'"},
            'category': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '16'}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'datetime': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastedit': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'txinfo': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['radiomon']
    symmetrical = True
