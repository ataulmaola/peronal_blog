from django.contrib import admin
from .models import BlogClass,Contact
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
	list_display=['__unicode__','updated','timestamp']
	list_display_links=['updated']
	list_filter=['updated','timestamp']
	search_fields=['title','content']
	class Meta:
		model=BlogClass

admin.site.register(BlogClass,BlogAdmin)

class ContactAdmin(admin.ModelAdmin):
	list_display=['__unicode__','name','phone']
	search_fields=['name','phone']
	class Meta:
		model=Contact

admin.site.register(Contact,ContactAdmin)