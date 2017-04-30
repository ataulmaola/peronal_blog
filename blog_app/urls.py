from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from blog_app.views import (blog_create,blog_list,blog_detail,blog_update,blog_delete,about,contact)
urlpatterns = [

    
    url(r'^create/$',blog_create,name="create"),
    url(r'^about/$',about,name="about"),
    url(r'^contact/$',contact,name="contact"),
    url(r'^(?P<slug>[\w-]+)/$',blog_detail,name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$',blog_update,name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$',blog_delete,name="delete"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
