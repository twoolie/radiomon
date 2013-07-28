# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Channel'
        db.create_table(u'radiomon_channel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True)),
            ('frequency', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('threshold', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('chop_from_start', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('initial_timeout', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.create_unique('radiomon_channel', ['short_name'])
        db.send_create_signal(u'radiomon', ['Channel'])

        # Adding model 'Transmission'
        db.create_table(u'radiomon_transmission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radiomon.Channel'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('transcript', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('segments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'radiomon', ['Transmission'])

        # Adding model 'Segment'
        db.create_table(u'radiomon_segment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transmission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['radiomon.Channel'])),
            ('start_timecode', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('end_timecode', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.create_unique(u'radiomon_segment', [u'transmission', 'start_timecode'])
        db.create_unique(u'radiomon_segment', [u'transmission', 'end_timecode'])
        db.send_create_signal(u'radiomon', ['Segment'])

    def backwards(self, orm):
        # Deleting model 'Channel'
        db.delete_unique('radiomon_channel', ['short_name'])
        db.delete_table(u'radiomon_channel')

        # Deleting model 'Transmission'
        db.delete_table(u'radiomon_transmission')



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
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
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
