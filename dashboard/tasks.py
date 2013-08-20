import logging

from celery import Celery
from celery.task import periodic_task
from celery.task import task
from datetime import timedelta, datetime
from os import environ

from trollop import TrelloConnection

from .models import Person, Board, List, Story

REDIS_URL = environ.get('REDISTOGO_URL', 'redis://localhost:6379')

celery = Celery('tasks', broker=REDIS_URL)

def get_story_data():
	conn = TrelloConnection('69387d468622b15d7a0a571e8165a793', 
							'c2021799351a98257f7cfde07b51d599434794eecf02c4923515769d0a5bbefc')
	hackathon = conn.me.boards[0]
	board_members = hackathon.members
	for member in board_members:
		exists = Person.objects.filter(name=member.fullname)
		if not exists:
			p = Person(name=member.fullname)
			p.save()

	board_exists = Board.objects.filter(title=hackathon.name)
	if not board_exists:
		b = Board(title=hackathon.name)

	for list in hackathon.lists:
		exists = List.objects.filter(title=list.name)
		if not exists:
			l = List(title=list.name, board=Board.objects.get(title=list.board.name))

	for story in hackathon.cards:
		exists = Story.objects.filter(title=story.name)
		if not exists:
			s = Story(title=story.name,
					  description=story.desc,
					  due_date=story.badges['due'],
					  current_list=List.objects.get(title=story.list),
					  board=Board.objects.get(title=story.board),
					  updated=datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))