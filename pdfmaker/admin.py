from adminsortable.admin import SortableAdmin, SortableTabularInline
from pdfmaker.models import Sow, Content, UserProfile
from django.contrib import admin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import makepdf
from django.contrib.auth.models import User


class ContentInline(SortableTabularInline):
	model = Content

class SowAdmin(SortableAdmin):
	fieldsets = [
		(None, {'fields': ['author']}),
		(None, {'fields': ['project']}),
		(None, {'fields': ['client']}),
		('Date published', {'fields': ['pub_date']})
	]
	list_display = ['project','client','pub_date','author']
	list_filter = ['author','pub_date','project']
	inlines = [ContentInline]
	actions = ['publish_pdf']

	
	def publish_pdf(self,request,queryset):
		for sow in queryset:
			sectionset = sow.content_set.order_by('order')
			makepdf.printpdf(sow,sectionset)
	publish_pdf.short_description = "Publish as .pdf"
	
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
