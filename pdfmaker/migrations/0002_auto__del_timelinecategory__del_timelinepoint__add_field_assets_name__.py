# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TimelineCategory'
        db.delete_table('pdfmaker_timelinecategory')

        # Deleting model 'TimelinePoint'
        db.delete_table('pdfmaker_timelinepoint')

        # Adding field 'Assets.name'
        db.add_column('pdfmaker_assets', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sow.client_contact'
        db.add_column('pdfmaker_sow', 'client_contact',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Milestones.description'
        db.alter_column('pdfmaker_milestones', 'description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Milestones.milestone_date'
        db.alter_column('pdfmaker_milestones', 'milestone_date', self.gf('django.db.models.fields.DateField')(null=True))
    def backwards(self, orm):
        # Adding model 'TimelineCategory'
        db.create_table('pdfmaker_timelinecategory', (
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('timeline', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['pdfmaker.Timeline'])),
            ('categoryname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('pdfmaker', ['TimelineCategory'])

        # Adding model 'TimelinePoint'
        db.create_table('pdfmaker_timelinepoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pointname', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('pdfmaker', ['TimelinePoint'])

        # Deleting field 'Assets.name'
        db.delete_column('pdfmaker_assets', 'name')

        # Deleting field 'Sow.client_contact'
        db.delete_column('pdfmaker_sow', 'client_contact')


        # Changing field 'Milestones.description'
        db.alter_column('pdfmaker_milestones', 'description', self.gf('django.db.models.fields.CharField')(default='description', max_length=255))

        # Changing field 'Milestones.milestone_date'
        db.alter_column('pdfmaker_milestones', 'milestone_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 7, 27, 0, 0)))
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pdfmaker.assets': {
            'Meta': {'object_name': 'Assets'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'pdfmaker.content': {
            'Meta': {'ordering': "['order']", 'object_name': 'Content'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'sectioncontent': ('django.db.models.fields.TextField', [], {}),
            'sectiontitle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.Sow']"})
        },
        'pdfmaker.milestones': {
            'Meta': {'object_name': 'Milestones'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.Timeline']"})
        },
        'pdfmaker.sow': {
            'Meta': {'object_name': 'Sow'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.UserProfile']"}),
            'client': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'client_contact': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.Assets']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'pdfmaker.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.UserProfile']"}),
            'client': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'pdfmaker.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['pdfmaker']