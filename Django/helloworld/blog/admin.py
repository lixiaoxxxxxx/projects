from django.contrib import admin
from blog.models import *

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title', 'date')
	search_fields = ('title', 'date')
	fields = ('title', 'date', 'content', 'cate')

admin.site.register(Cata)
admin.site.register(Blog, BlogAdmin)
