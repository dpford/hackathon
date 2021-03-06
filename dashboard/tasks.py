import logging

from celery import Celery
from celery.task import periodic_task
from celery.task import task
from datetime import timedelta, datetime
from os import environ

from trollop import TrelloConnection

from .models import Person, Board, List, Story, Action

REDIS_URL = environ.get('REDISTOGO_URL', 'redis://localhost:6379')

celery = Celery('tasks', broker=REDIS_URL)

def get_story_data():
	conn = TrelloConnection('69387d468622b15d7a0a571e8165a793', 
							'c2021799351a98257f7cfde07b51d599434794eecf02c4923515769d0a5bbefc')
	hackathon = conn.me.boards[0]
	board_members = hackathon.members
	for member in board_members:
		exists = Person.objects.filter(trello_id=member._id)
		if not exists:
			p = Person(name=member.fullname, 
					   username=member.username, 
					   trello_id=member._id)
			p.save()

	board_exists = Board.objects.filter(trello_id=hackathon._id)
	if not board_exists:
		b = Board(title=hackathon.name, trello_id=hackathon._id,
			updated = datetime.strptime(hackathon._data['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ"))
		b.save()

	for list in hackathon.lists:
		exists = List.objects.filter(trello_id=list._id)
		if not exists:
			l = List(title=list.name, 
					 board=Board.objects.get(trello_id=list.board._id),
					 trello_id=list._id)
			l.save()

	for story in hackathon.cards:
		exists = Story.objects.filter(trello_id=story._id)
		
		if not exists:
			persons = []
			if story.members:
				for member in story.members:
					persons.append(Person.objects.get(trello_id=member._id).pk)
			due_date = None
			if story.badges['due']:
				due_date = datetime.strptime(story.badges['due'], "%Y-%m-%dT%H:%M:%S.%fZ")
			s = Story(title=story.name,
					  description=story.desc,
					  due_date=due_date,
					  current_list=List.objects.get(trello_id=story.list._id),
					  board=Board.objects.get(trello_id=story.board._id),
					  updated=datetime.strptime(story._data['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ"),
					  trello_id=story._id)
			s.save()
			s.persons = persons
		elif Story.objects.get(trello_id=story._id).updated < datetime.strptime(story._data['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ"):
			print "ok got past the elif"
			persons = []
			if story.members:
				for member in story.members:
					persons.append(Person.objects.get(trello_id=member._id).pk)
			due_date = None
			if story.badges['due']:
				due_date = datetime.strptime(story.badges['due'], "%Y-%m-%dT%H:%M:%S.%fZ")
			this_story = Story.objects.get(trello_id=story._id)
			this_story.title = story.name
			this_story.description = story.desc
			this_story.due_date = due_date
			this_story.current_list = List.objects.get(title=story.list.name)
			this_story.board = Board.objects.get(trello_id=story.board._id)
			this_story.updated = datetime.strptime(story._data['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ")
			this_story.save()
			this_story.persons = persons

def get_actions():
	conn = TrelloConnection('69387d468622b15d7a0a571e8165a793', 
							'c2021799351a98257f7cfde07b51d599434794eecf02c4923515769d0a5bbefc')
	hackathon = conn.me.boards[0]
	for action in hackathon.actions:
		exists = Action.objects.filter(trello_id=action._data['id'])
		if 'board' in action._data['data']:
			has_board = Board.objects.filter(trello_id=action._data['data']['board']['id'])
		else:
			print "this happened"
			has_board = True
		if has_board and not exists:
			if 'card' in action._data['data']:
				story_id = action._data['data']['card']['id']
				this_story = Story.objects.get(trello_id=story_id)
			else:
				this_story = None
			if has_board == True:
				this_board = None
			else:
				this_board = Board.objects.get(trello_id=action._data['data']['board']['id'])
			a = Action(type=action._data['type'],
					   person=Person.objects.get(trello_id=action._data['idMemberCreator']),
					   trello_id=action._data['id'],
					   story=this_story,
					   board=this_board,
					   date=datetime.strptime(action._data['date'], "%Y-%m-%dT%H:%M:%S.%fZ"))
			a.save()



@periodic_task(run_every=timedelta(seconds=30))
def trello_data():
    get_story_data()
    get_actions()