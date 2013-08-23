from django.db import models

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	trello_id = models.CharField(max_length=100)

	def stories(self):
		return Story.objects.filter(persons__in=[self])

	def __unicode__(self):
		return self.name

class Board(models.Model):
	title = models.CharField(max_length=100)
	trello_id = models.CharField(max_length=100)
	updated = models.DateTimeField()

	def __unicode__(self):
		return self.title

class List(models.Model):
	title = models.CharField(max_length=100)
	board = models.ForeignKey(Board)
	trello_id = models.CharField(max_length=100)

	def stories(self):
		return Story.objects.filter(current_list=self)

	def __unicode__(self):
		return self.title


class Story(models.Model):

	title = models.CharField(max_length=300)
	description = models.TextField()
	persons = models.ManyToManyField(Person, blank=True)
	due_date = models.DateField(blank=True, null=True)
	current_list = models.ForeignKey(List)
	board = models.ForeignKey(Board)
	updated = models.DateTimeField()
	trello_id = models.CharField(max_length=100)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name_plural = "stories"

class Action(models.Model):
	type = models.CharField(max_length=300)
	person = models.ForeignKey(Person)
	trello_id = models.CharField(max_length=100)
	story = models.ForeignKey(Story, blank=True, null=True)
	board = models.ForeignKey(Board, blank=True, null=True)
	date = models.DateTimeField()

	def __unicode__(self):
		return "%s performed a %s" % (self.person, self.type)