from adminsortable.admin import SortableAdmin, SortableTabularInline
from pdfmaker.models import Sow, Content, UserProfile, Assets
from django.contrib import admin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import makepdf
from django.contrib.auth.models import User
from django.core.files import File

class AssetInline(admin.TabularInline):
	model = Assets
	extra = 0

class ContentInline(SortableTabularInline):
	model = Content
	extra = 2

class SowAdmin(SortableAdmin):

	
	fieldsets = [
		(None, {'fields': ['author']}),
		(None, {'fields': ['project']}),
		(None, {'fields': ['client']}),
		('Date published', {'fields': ['pub_date']}),
	]
	list_display = ('project','client','pub_date','author','show_pdf_url')
	list_filter = ['author','pub_date','project']
	inlines = [AssetInline,ContentInline]
	actions = ['publish_pdf']

	def publish_pdf(self,request,queryset):
		for sow in queryset:
			sectionset = sow.content_set.order_by('order')
			img = sow.assets.img
			makepdf.printpdf(sow,sectionset)
	publish_pdf.short_description = "Publish as .pdf"
	
	def show_pdf_url(self,obj):
		name = obj.pdflink()
		return '<a href="/media/{}">{}</a>'.format(name,name)
	show_pdf_url.allow_tags = True
	
	
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
admin.site.register(Sow, SowAdmin, Media=CommonMedia)
