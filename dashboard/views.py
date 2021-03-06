from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Person, Story, Board, List, Action, ExcelloUser

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
    if request.user.is_authenticated():
        if ExcelloUser.objects.filter(username=request.user.username):
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('setup'))

    # get data for people/story breakdown
    person_count = {}
    for person in Person.objects.select_related():
        person_count[person.name] = 0

    person_list_count = {}
    for list in List.objects.all():
        person_list_count[list.title] = person_count.copy()

    for person in Person.objects.select_related():
        for story in person.stories():
            person_list_count[story.current_list.title][person.name] += 1

    # create data for pie chart

    list_percentages = []
    total_stories = Story.objects.all().count() * 1.0 # turn into float
    for list in List.objects.all():
        percent_this_story = (list.stories().count() / total_stories) * 100
        list_percentages.append([list.title, percent_this_story])

    # create data for action activity

    list_action_counts = []
    for person in Person.objects.all():
        one_week = len(Action.objects.filter(person=person, 
                                             date__gt=(datetime.datetime.now() - datetime.timedelta(days=7))))
        two_week = len(Action.objects.filter(person=person, 
                                             date__gt=(datetime.datetime.now() - datetime.timedelta(days=14)),
                                             date__lt=(datetime.datetime.now() - datetime.timedelta(days=7))))
        three_week = len(Action.objects.filter(person=person, 
                                             date__gt=(datetime.datetime.now() - datetime.timedelta(days=21)),
                                             date__lt=(datetime.datetime.now() - datetime.timedelta(days=14))))
        four_week = len(Action.objects.filter(person=person, 
                                             date__gt=(datetime.datetime.now() - datetime.timedelta(days=28)),
                                             date__lt=(datetime.datetime.now() - datetime.timedelta(days=21))))
        list_action_counts.append([person.name, [one_week, two_week, three_week, four_week]])


    return render(request, 'index.html',
                  {'persons' : Person.objects.all(),
                  'lists' : List.objects.all(),
                  'stories' : Story.objects.all(),
                  'boards' : Board.objects.all(),
                  'person_list_count' : person_list_count,
                  'list_percentages' : list_percentages,
                  'late_stories' : Story.objects.filter(due_date__lt=datetime.date.today()).exclude(current_list__title='Done'),
                  'list_action_counts' : list_action_counts})

def about(request):
    return render(request, 'about.html', {})

def login(request):
    return render(request, 'login.html', {})

@login_required
def setup(request):
    oauth_id = request.user.social_auth.filter(provider='trello')[0].extra_data['access_token']['oauth_token']
    conn = TrelloConnection(settings.SOCIAL_AUTH_TRELLO_KEY, oauth_id)
    boards = conn.me.boards
    return render(request, 'setup.html', {'boards': boards})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})