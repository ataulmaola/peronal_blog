from django import forms
from .models import BlogClass,Contact



class PostBlog(forms.ModelForm):
	"""docstring for ClassName"""
	class Meta:
		model=BlogClass
		fields=[
            'title',
            'content',
            'image',
            'draft',
            'publish', 
		]
class ContactForm(forms.ModelForm):
	"""docstring for ClassName"""
	class Meta:
		model=Contact
		fields=[
            'name',
            'email',
            'phone',
            'city',
            'message', 
		]
