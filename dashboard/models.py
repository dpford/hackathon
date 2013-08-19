from django.db import models

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Story(models.Model):

	STATUS_CHOICES = (
	    (1, "Backlog"),
	    (2, "Doing"),
	    (3, "Done"),
	)


	title = models.CharField(max_length=300)
	description = models.TextField()
	persons = models.ForeignKey(Person)
	due_date = models.DateField()
	status = models.IntegerField(choices=STATUS_CHOICES)

	def __unicode__(self):
		return "Story: %s" % (self.title,)

class Board(models.Model):
	title = models.CharField(max_length=100)

	def __unicode__(self):
		return "Board: %s" % (self.title)