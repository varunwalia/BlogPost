# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ['title' , 'created' , 'modified']
	list_filter = ['modified' , 'created']
	list_display_links = ['title']
	search_fields = ['title']

	class Meta:
		model = Post

admin.site.register(Post , PostAdmin)