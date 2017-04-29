# try:
# 	from urllib import quote_plus
# except:
# 	pass
# try:
# 	from urllib.parse import quote_plus
# except:
# 	pass

from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404 ,redirect
from django.utils import timezone
from .models import BlogClass

from .forms import PostBlog,ContactForm
# Create your views here.


#This is for creating blog post
def blog_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostBlog(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user=request.user
		instance.save()
		#messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context={
	    "form":form,
	}
	return render(request,'post_form.html',context)



#This is for  blog post Detail
def blog_detail(request,slug=None):
	instance=get_object_or_404(BlogClass,slug=slug)
	if instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	#share_string=quote_plus(instance.content)
	context={
	   "blog_title":instance.title,
	   "instance":instance,
	   #"share_string":share_string,
	}
	return render(request,'post_detail.html',context)



#This is for  blog post List
def blog_list(request):
	query_set_list=BlogClass.objects.active() #.order_by("-timestamp")
	if  request.user.is_staff or  request.user.is_superuser:
		query_set_list=BlogClass.objects.all()
	query=request.GET.get("q")
	if query:
		query_set_list=BlogClass.objects.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	page_request_var="page"
	paginator = Paginator(query_set_list, 4) # Show 25 contacts per page
	page = request.GET.get(page_request_var)
	try:
		query_set = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		query_set = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		query_set=paginator.page(paginator.num_pages)
	context={
	   "title":"ATAUL's Blog",
	   "query_set":query_set,
	   "page_request_var":page_request_var,
	}

	return render(request,'show_list.html',context)


#This is for  blog post Update/edit
def blog_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(BlogClass,slug=slug)
	form=PostBlog(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Edited")
		return HttpResponseRedirect(instance.get_absolute_url())	
	context={
	   "blog_title":instance.title,
	   "instance":instance,
	   "form":form,
	}
	return render(request,'post_form.html',context)



#This is for  blog post deletation
def blog_delete(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(BlogClass,slug=slug)
	instance.delete()
	messages.success(request,"Successfully Deleted")	
	return redirect("blog_app:list")

def about(request):
	title="About Me"
	context={
	  "blog_about":title,
	}
	return render(request,'about.html',context)

def contact(request):
	title="Conatct Me"
	form=ContactForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user=request.user
		instance.save()
		messages.success(request,"Successfully Created")
		return redirect("blog_app:list")
	context={
	  "blog_contact":title,
	   "form":form,
	}
	return render(request,'contact.html',context)