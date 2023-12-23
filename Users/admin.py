from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AppUser)
admin.site.register(Edu)
admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(PostLikes)
admin.site.register(Report)
admin.site.register(Follow)
admin.site.register(Message)
admin.site.register(Color)