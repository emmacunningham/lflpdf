from django.db import models
from django.contrib.auth.models import User
from adminsortable.models import Sortable, SortableForeignKey
from django.db.models.signals import post_save


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	phone = models.CharField(max_length=255,blank=True)
	
	def __unicode__(self):
		return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
		
post_save.connect(create_user_profile, sender=User)


class Assets(models.Model):
	img = models.FileField(upload_to='img/',blank=True,null=True)
	
	def __unicode__(self):
		return self.img.name


class Sow(Sortable):
	class Meta:
		pass
	project = models.CharField(max_length=255)
	client = models.CharField(max_length=255)
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(UserProfile)
	pdf = models.FileField(upload_to='pdf/sow',blank=True,null=True)
	img = models.ForeignKey(Assets,blank=True,null=True)
		
	def __unicode__(self):
		return self.project

class Content(Sortable):
	class Meta(Sortable.Meta):
		pass
	sow = models.ForeignKey(Sow)
	sectiontitle = models.CharField(max_length=255)
	sectioncontent = models.TextField()

	def __unicode__(self):
		return self.sectiontitle

class Timeline(Sortable):
	class Meta:
		pass
	project = models.CharField(max_length=255)
	client = models.CharField(max_length=255)
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(UserProfile)
	pdf = models.FileField(upload_to='pdf/timeline',blank=True,null=True)
	
	def __unicode__(self):
		return self.project
		
class Milestones(Sortable):
	class Meta:
		pass
	timeline = models.ForeignKey(Timeline)
	description = models.CharField(max_length=255,null=True)
	milestone_date = models.DateField('milestone date',null=True)
	
	def __unicode__(self):
		return self.description

class TimelineCategory(Sortable):
	categoryname = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.categoryname
	
class TimelinePoint(Sortable):
	timeline = models.ForeignKey(Timeline)
	timelinecategory = models.ForeignKey(TimelineCategory)
	pointinformation = models.CharField(max_length=255)
	datestart = models.DateField('start date',null=True)
	datehighstart = models.DateField('high start date',null=True,blank=True)
	dateend = models.DateField('end date',blank=True,null=True)
	
	def __unicode__(self):
		return self.pointinformation