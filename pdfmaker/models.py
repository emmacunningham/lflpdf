from django.db import models
from django.contrib.auth.models import User
from adminsortable.models import Sortable, SortableForeignKey
from django.db.models.signals import post_save

AGENCY_SIGNATURE_CHOICES = (
    ('Sarah Richardson', 'Sarah Richardson'),
    ('Eric Lee', 'Eric Lee'),
)

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
	name = models.CharField(max_length=255,blank=True,null=True)
	
	def __unicode__(self):
		return self.img.name


class Sow(Sortable):
	class Meta:
		pass
	project = models.CharField(max_length=255)
	client = models.CharField(max_length=255)
	client_contact = models.CharField(max_length=255,blank=True,null=True)
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(UserProfile)
	agency_signature =  models.CharField(max_length=255,choices=AGENCY_SIGNATURE_CHOICES,default='Sarah Richardson')
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


