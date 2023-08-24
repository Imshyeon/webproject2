from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Group, User

# Register your models here.
admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model=User
    fields = ['username','first_name','last_name','email']
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User,UserAdmin)

