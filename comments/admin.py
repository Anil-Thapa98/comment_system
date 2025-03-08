from django.contrib import admin
 

from .models import Comment, Blog, Notification
 
admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(Notification)

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified', 'bio', 'location')
    search_fields = ('user__username', 'bio', 'location')
