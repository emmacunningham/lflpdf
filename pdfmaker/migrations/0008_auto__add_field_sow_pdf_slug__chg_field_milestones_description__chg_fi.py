# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sow.pdf_slug'
        db.add_column('pdfmaker_sow', 'pdf_slug',
                      self.gf('django.db.models.fields.SlugField')(default='slug', max_length=50),
                      keep_default=False)


        # Changing field 'Milestones.description'
        db.alter_column('pdfmaker_milestones', 'description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Milestones.milestone_date'
        db.alter_column('pdfmaker_milestones', 'milestone_date', self.gf('django.db.models.fields.DateField')(null=True))
    def backwards(self, orm):
        # Deleting field 'Sow.pdf_slug'
        db.delete_column('pdfmaker_sow', 'pdf_slug')


        # Changing field 'Milestones.description'
        db.alter_column('pdfmaker_milestones', 'description', self.gf('django.db.models.fields.CharField')(default='description', max_length=255))

        # Changing field 'Milestones.milestone_date'
        db.alter_column('pdfmaker_milestones', 'milestone_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 1, 0, 0)))
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
            'img': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.Assets']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
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
        'pdfmaker.timelinecategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'TimelineCategory'},
            'categoryname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        'pdfmaker.timelinepoint': {
            'Meta': {'ordering': "['order']", 'object_name': 'TimelinePoint'},
            'dateend': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'datehighstart': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'datestart': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'pointinformation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.Timeline']"}),
            'timelinecategory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdfmaker.TimelineCategory']"})
        },
        'pdfmaker.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['pdfmaker']