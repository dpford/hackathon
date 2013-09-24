from django.contrib import admin

from .models import Person, Story, Board, List, Action, ExcelloUser

class PersonAdmin(admin.ModelAdmin):
	list_display = ('name',)

class StoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'due_date', 'updated',)

class BoardAdmin(admin.ModelAdmin):
	list_display = ('title',)

class ListAdmin(admin.ModelAdmin):
	list_display = ('title', 'board',)

class ActionAdmin(admin.ModelAdmin):
	list_display = ('type', 'person', 'date', 'story', 'board',)

class ExcelloUserAdmin(admin.ModelAdmin):
	list_display = ('email', 'first_name', 'last_name', 'date_joined')

admin.site.register(Person, PersonAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ExcelloUser, ExcelloUserAdmin)