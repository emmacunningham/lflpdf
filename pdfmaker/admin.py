from adminsortable.admin import SortableAdmin, SortableTabularInline
from pdfmaker.models import Sow, Content, UserProfile, Assets, Timeline, Milestones
from django.contrib import admin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import makesow
import maketimeline
from django.contrib.auth.models import User
from django.core.files import File

class ContentInline(SortableTabularInline):
	model = Content
	extra = 2
	
class SowAdmin(SortableAdmin):
	fieldsets = [
		(None, {'fields': ['author', 'agency_signature']}),
		(None, {'fields': ['project']}),
		(None, {'fields': ['client', 'client_contact']}),
		('Date published', {'fields': ['pub_date']}),
		('Side image', {'fields': ['img']})
	]
	list_display = ('project','client','pub_date','author','show_pdf_url')
	list_filter = ['author','pub_date','project']
	inlines = [ContentInline]
	actions = ['publish_pdf']

	def publish_pdf(self,request,queryset):
		for sow in queryset:
			sectionset = sow.content_set.order_by('order')
			makesow.printpdf(sow,sectionset)
	publish_pdf.short_description = "Publish as .pdf"
	
	def show_pdf_url(self,obj):
		if obj.pdf:
			return '<a href="{0}">{1}</a>'.format(obj.pdf.url,obj.pdf.url)
		else:
			return 'no published pdf yet'
	show_pdf_url.allow_tags = True
	
class MilestoneInline(SortableTabularInline):
	model = Milestones
	extra = 2

class TimelineAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['author']}),
		(None, {'fields': ['project']}),
		(None, {'fields': ['client']}),
		('Date published', {'fields': ['pub_date']}),
	]
	list_display = ('project','client','pub_date','author','show_pdf_url')
	list_filter = ['author','pub_date','project']
	inlines = [MilestoneInline]
	actions = ['publish_pdf']

	def publish_pdf(self,request,queryset):
		for timeline in queryset:
			timelineset = timeline.timelinepoint_set.all()
			maketimeline.printpdf(timeline,timelineset)
	publish_pdf.short_description = "Publish as .pdf"
	
	def show_pdf_url(self,obj):
		if obj.pdf:
			return '<a href="{}">{}</a>'.format(obj.pdf.url,obj.pdf.url)
		else:
			return 'no published pdf yet'
	show_pdf_url.allow_tags = True
	
class AssetAdmin(admin.ModelAdmin):
	fieldsets = [('Upload an image',{'fields':['img']})]
	
class CommonMedia:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    'http://some-antics.com/emma/appmedia/admin/js/editor.js',
    )
  css = {
    'all': ('http://some-antics.com/emma/appmedia/admin/css/editor.css',),
  }	

class UserProfileInline(admin.TabularInline):
	model = UserProfile

class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'first_name', 'last_name', 'email']
	inlines = [UserProfileInline]

admin.site.unregister(User)	
admin.site.register(User, UserAdmin)
admin.site.register(Assets, AssetAdmin)
admin.site.register(Sow, SowAdmin, Media=CommonMedia)

# Commenting out timeline admin until it's finished.
#admin.site.register(Timeline, TimelineAdmin)
