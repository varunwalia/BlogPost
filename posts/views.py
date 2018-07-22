# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urllib import quote_plus
from django.http import HttpResponse , HttpResponseRedirect , Http404 
from django.shortcuts import render , get_object_or_404 , redirect

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType


from comments.models import Comments
from comments.forms  import CommentForm

from .models import Post
from .forms import PostForm
# Create your views here.

def page(request):
	return render(request , 'home.html' , {})


def Create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None , request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = request.user
		instance.save()
		messages.success(request , "<a href='#'> Post </a> Successfully Created" , extra_tags = 'html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())


	context = {'form':form}
	return render(request , 'create.html' , context)

# def Detail(request , slug =None):
# 	queryset = get_object_or_404(Post , slug =slug)
# 	if queryset.draft or queryset.publish > timezone.now().date():
# 		if not request.user.is_staff or not request.user.is_superuser:
# 			raise Http404
# 	share_string  = quote_plus(queryset.content)

# 	# content_type = ContentType.objects.get_for_model(Post)
# 	# object_id = queryset.id

# 	initial_data = {
# 		'content_type' : queryset.get_content_type ,
# 		'object_id' : queryset.id ,
# 		}
# 	form = CommentForm(request.POST or None , initial = initial_data)

# 	if form.is_valid():
# 		c_type = form.cleaned_data.get("content_type")
# 		content_type = ContentType.objects.get( model = c_type)
#  		obj_id = form.cleaned_data.get('object_id')
# 		content_data = form.cleaned_data.get("content")
# 		new_comment , created = Comments.objects.get_or_create(
# 				user = request.user ,
# 				content_type = content_type ,
# 				object_id=  obj_id,
# 				content = content ,
# 			)
# 		if created:
# 			print("Yes	")
# 		# print(comment_form.cleaned_data)
	

# 	comments = queryset.comments
# 	context = {'queryset':queryset ,
# 				 'share_string':share_string,
# 				 'comments' : comments,
# 				 'comment_form':form,

# 				 }

# 	return render(request , 'detail.html' , context)


def Detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get( model= c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comments.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							# parent = parent_obj,
						)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	comments = instance.comments
	context = {
		
		"queryset": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
	}
	return render(request, "detail.html", context)

def Update(request,  slug):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post , slug = slug)
	form = PostForm(request.POST or None , request.FILES or None ,instance = instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request , "<a href='#'> Post </a> Successfully Created" , extra_tags = 'html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	return render(request , 'create.html' , {'form':form})

def Delete(request , slug = None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post , slug =slug)
	instance.delete()
	messages.success(request , "Post Successfully Deleted")
	return redirect('posts:List')

def List(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active()

	
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all() 
	

	query = request.GET.get('q')
	if query:
		queryset_list = Post.objects.active().filter(Q(title__icontains  = query) |
													 Q(content__icontains  = query) |
													 Q(user__first_name__icontains  = query) |
													 Q(user__last_name__icontains  = query)).distinct() 

  #filter(draft = False).filter(publish__lte = timezone.now())      #all().order_by('-created')
	paginator = Paginator(queryset_list, 3) # Show 25 quersets per page
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	return render(request , 'list.html' , {'today':today ,
	   										'queryset': queryset ,
	  									'page_request_var':page_request_var})


