from django.contrib import admin

from user.models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
	fieldsets = [
		('user', {'fields':['user']}),
		('imsi', {'fields':['imsi']}),
		('version count', {'fields':['version_count']}),
	]
admin.site.register(UserInfo,UserInfoAdmin)