from django.contrib import admin

from .models import Person, Story, Board

class PersonAdmin(admin.ModelAdmin):
	list_display = ('name',)

class StoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'persons', 'due_date',)

class BoardAdmin(admin.ModelAdmin):
	list_display = ('title',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Board, BoardAdmin)