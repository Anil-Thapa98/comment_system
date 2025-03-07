from django.contrib import admin
 

from .models import Comment, Blog, Notification
 
admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(Notification)
 
