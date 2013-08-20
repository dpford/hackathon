from django.contrib import admin

from .models import Person, Story, Board, List

class PersonAdmin(admin.ModelAdmin):
	list_display = ('name',)

class StoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'due_date',)

class BoardAdmin(admin.ModelAdmin):
	list_display = ('title',)

class ListAdmin(admin.ModelAdmin):
	list_display = ('title', 'board',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(List, ListAdmin)