from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

class BlogManager(models.Manager):
	def active(self,*args,**kwargs):
		#BlogClass.objects.all()=super(BlogManager,self).all()
		return super(BlogManager,self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)

class BlogClass(models.Model):
	"""docstring for ClassName"""
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	title=models.CharField(max_length=500)
	slug=models.SlugField(unique=True)
	image=models.ImageField(upload_to=upload_location,null=True,blank=True,height_field="height_field",width_field="width_field")
	height_field=models.IntegerField(default=0)
	width_field=models.IntegerField(default=0)
	content=models.TextField()
	draft=models.BooleanField(default=False)
	publish=models.DateField(auto_now=False,auto_now_add=False)
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)

	objects=BlogManager()

	def __unicode__(self):
		return self.title
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blog_app:detail",kwargs={"slug":self.slug})
	class Meta:
		ordering=["-timestamp","-updated"]


class Contact(models.Model):
	"""docstring for ClassName"""
	name=models.CharField(max_length=70)
	email=models.EmailField(max_length=100)
	phone=models.CharField(max_length=15)
	city=models.CharField(max_length=50)
	message=models.TextField()
	def __unicode__(self):
		return self.email
	def __str__(self):
		return self.email

	

def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs=BlogClass.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug="%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug

	

def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance) 


pre_save.connect(pre_save_post_receiver,sender=BlogClass)

