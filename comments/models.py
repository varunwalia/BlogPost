# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import  python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from django.db import models



# Create your models here.

class CommentManager(models.Manager):
	def filter_by_instance(self , instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)  # Post
		object_id = instance.id
		qs = super(CommentManager , self).filter(content_type = content_type,  object_id = object_id)
		return qs

		 # super(CommentManager , self) ---> Comments.object



class Comments(models.Model):

	user 			= models.ForeignKey(settings.AUTH_USER_MODEL , default = 1)
	# post            = models.ForeignKey(Post)

	content_type 	= models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id	    = models.PositiveIntegerField()
	content_object  = GenericForeignKey('content_type', 'object_id')

	parent = models.ForeignKey("self" , null=True,blank="True")

	content         = models.TextField()
	timestamp       = models.DateTimeField(auto_now_add = True)

	objects = CommentManager()

	def __str__(self):
		return  str(self.user.username)

	class Meta:
		verbose_name = 'Comments'
		verbose_name_plural = 'Comments'
		ordering = ['-timestamp']


	def children(self): #replies
		return Comments.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True