from django.contrib import admin

from ball.models import Ball

class BallAdmin(admin.ModelAdmin):
	fieldsets = [
		('user', {'fields':['user']}),
		('catcher', {'fields':['catcher']}),
		('begin location', {'fields':['current_lat', 'current_lng']}),
		('end location', {'fields':['end_lat', 'end_lng']}),
		('begin date', {'fields':['date']}),
		('end date', {'fields':['end_date']}),
		('ball status', {'fields':['ball_status']}),
		('ball type', {'fields':['ball_type']})
	]
admin.site.register(Ball,BallAdmin)