# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.utils.encoding import  python_2_unicode_compatible	
from django.db import models
from utils.models import CreationModificationDateMixin
from django.core.urlresolvers import reverse
from django.utils.timezone import now as timezone_now
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.safestring import mark_safe	


from markdown_deux import markdown

from comments.models import Comments




# Create your models here.



# def upload_location(instance , filename):
# 	# filebase , extension = filename.split('.')
# 	# return"%s/%s.%s" %(instance.id , instance.id , filename)
# 	return"%s/%s" %(strftime(%a), filename)

#Post.objects.all() =  super(PostManager , self).all() << Essentially the same

# all >> active >> can be anything
class PostManager(models.Manager):
	def active(self , *args , **kwargs):
		return super(PostManager , self).filter(draft = False).filter(publish__lte = timezone_now())

def upload_location(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return "blogs/%s/%s/%s" % (
        now.strftime("%Y"),
        now.strftime("%B"),
        filename,
    )



class Post(CreationModificationDateMixin ,   models.Model):
	user  = models.ForeignKey(settings.AUTH_USER_MODEL , default=1)
	title = models.CharField(max_length = 120)
	slug  = models.SlugField(unique = True)
	image = models.ImageField(   upload_to = upload_location,
										null= True , blank = True ,
										width_field = 'width_field' ,
		  								height_field = 'height_field')
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default=0)
	content =  models.TextField()
	draft = models.BooleanField(default = False)
	publish = models.DateField(auto_now = False , auto_now_add = False)

	objects = PostManager()  #objects -- can be anything 
							 #if you change then in views change 
							 #qs = Post.change.all()


	def __str__(self):
		return self.title

	def get_absolute_url(self , **kwargs):
		return reverse('posts:Detail' , kwargs = {'slug': self.slug })

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'

	def get_markdown(self):
		content =  self.content
		return mark_safe(markdown(content))

	@property 
	def comments(self):
		
		instance = self
		qs 		 = Comments.objects.filter_by_instance(instance)
		return qs
	
	@property 
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type




def create_slug(instance , new_slug =None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug = slug).order_by('-pk')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug , qs.first().id)
		return create_slug(instance , new_slug = new_slug)
	return slug



def pre_save_post_receiver(sender , instance , *args , **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver , sender = "posts.Post")
