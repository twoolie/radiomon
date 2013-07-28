# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TransmissionInfo'
        db.create_table('transmissioninfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.CharField')(default='None', max_length=16)),
            ('lastedit', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('txinfo', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'radiomon', ['TransmissionInfo'])


    def backwards(self, orm):
        # Deleting model 'TransmissionInfo'
        db.delete_table('transmissioninfo')


    models = {
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