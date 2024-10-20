from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet
# Register your models here.

admin.site.unregister(Group)
admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
   model = User
   fields = ['username']
   inlines = [ProfileInline]
      
      
admin.site.register(User, UserAdmin)
admin.site.register(Tweet)


    