from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from .models import Person, Story, Board, List

from trollop import TrelloConnection

import datetime

@never_cache
def home(request):
    # data = {}
    # conn = TrelloConnection('69387d468622b15d7a0a571e8165a793', 'c2021799351a98257f7cfde07b51d599434794eecf02c4923515769d0a5bbefc')
    # hackathon = conn.me.boards[0]
    # board_members = hackathon.members
    
    # # Create a dict entry for each member
    # first = datetime.datetime.now()
    # mem_count = {}
    # for member in board_members:
    #     mem_count[member.fullname] = 0
    # print "first took " + str(datetime.datetime.now() - first)

    # # Populate dict
    # second = datetime.datetime.now()
    # for card in hackathon.cards:
    #     for member in card.members:
    #         blah = datetime.datetime.now()
    #         mem_count[member.fullname] += 1
    #         print "lookup took" + str(datetime.datetime.now() - blah)

    # print "second took " + str(datetime.datetime.now() - second)
 
    # data['assignments'] = mem_count
    
    # # Create an empty dict for each category
    # mem_categories = {}
    # for list in hackathon.lists:
    #     mem_categories[list.name] = 0

    
    
    # # Create a dict for each member with stories by category
    # start_categories = datetime.datetime.now()
    # adv_mem_count = {}
    # for member in board_members:
    #     adv_mem_count[member.fullname] = mem_categories.copy() #copy() to create a new reference
    # print "categories took " + str(datetime.datetime.now() - start_categories)
        
    # # Populate that dict with actual stories, broken out by category
    # start_breakout = datetime.datetime.now()
    # for card in hackathon.cards:
    #     for member in card.members:
    #         blah2 = datetime.datetime.now()
    #         adv_mem_count[member.fullname][card.list.name] += 1
    #         print "breakout lookup took " + str(datetime.datetime.now() - blah2)
    # print "breakout took " + str(datetime.datetime.now() - start_breakout)
            
    # data['adv_assignments'] = adv_mem_count

    # # Current status - count of each list
    # list_count = {}
    # for list in hackathon.lists:
    #     list_count[list.name] = len(list.cards)

    # data['list_count'] = list_count

    # # Overdue stories
    # todaydatetime = datetime.datetime.now()
    # todaydate = datetime.datetime.date(todaydatetime)
    # late_master = []
    # for card in hackathon.cards:
    #     if card._data['due'] and card.list.name != 'Done':
    #         duedatetime = datetime.datetime.strptime(card._data['due'][:19], '%Y-%m-%dT%H:%M:%S')
    #         duedate = datetime.datetime.date(duedatetime)
    #         if duedate <= todaydate:
    #             late_dict = {}
    #             late_members = []
    #             for member in card.members:
    #                 late_members.append(member.fullname)
    #             late_dict['members'] = late_members
    #             late_dict['title'] = card.name
    #             late_dict['description'] = card.desc
    #             late_dict['due'] = card._data['due'][:10]
    #             late_master.append(late_dict)
    # data['late_stories'] = late_master  


    # get data for people/story breakdown
    person_count = {}
    for person in Person.objects.all():
        person_count[person.name] = 0

    person_list_count = {}
    for list in List.objects.all():
        person_list_count[list.title] = person_count.copy()

    for person in Person.objects.all():
        for story in person.stories():
            person_list_count[story.current_list.title][person.name] += 1

    # create data for pie chart

    list_percentages =[]
    total_stories = Story.objects.all().count() * 1.0 # turn into float
    for list in List.objects.all():
        percent_this_story = (list.stories().count() / total_stories) * 100
        list_percentages.append([list.title, percent_this_story])

    print Story.objects.filter(due_date__lt=datetime.date.today())
    return render(request, 'index.html',
                  {'persons': Person.objects.all(),
                  'lists': List.objects.all(),
                  'stories': Story.objects.all(),
                  'boards': Board.objects.all(),
                  'person_list_count': person_list_count,
                  'list_percentages' : list_percentages,
                  'late_stories' : Story.objects.filter(due_date__lt=datetime.date.today())})