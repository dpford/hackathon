from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from trollop import TrelloConnection

import datetime

@never_cache
def home(request):
    data = {}
    conn = TrelloConnection('69387d468622b15d7a0a571e8165a793', 'c2021799351a98257f7cfde07b51d599434794eecf02c4923515769d0a5bbefc')
    hackathon = conn.me.boards[0]
    board_members = hackathon.members
    

    # Create a dict entry for each member
    mem_count = {}
    for member in board_members:
        mem_count[member.fullname] = 0

    # Populate dict
    for card in hackathon.cards:
        for member in card.members:
            mem_count[member.fullname] += 1
 
    data['assignments'] = mem_count
    
    # Create an empty dict for each category
    mem_categories = {}
    for list in hackathon.lists:
        mem_categories[list.name] = 0
    
    # Create a dict for each member with stories by category
    adv_mem_count = {}
    for member in board_members:
        adv_mem_count[member.fullname] = mem_categories.copy() #copy() to create a new reference
        
    # Populate that dict with actual stories, broken out by category
    for card in hackathon.cards:
        for member in card.members:
            adv_mem_count[member.fullname][card.list.name] += 1
            
    data['adv_assignments'] = adv_mem_count

    # Current status - count of each list
    list_count = {}
    for list in hackathon.lists:
        list_count[list.name] = len(list.cards)

    data['list_count'] = list_count

    # Overdue stories
    todaydatetime = datetime.datetime.now()
    todaydate = datetime.datetime.date(todaydatetime)
    late_master = []
    for card in hackathon.cards:
        if card._data['due'] and card.list.name != 'Done':
            duedatetime = datetime.datetime.strptime(card._data['due'][:19], '%Y-%m-%dT%H:%M:%S')
            duedate = datetime.datetime.date(duedatetime)
            if duedate <= todaydate:
                late_dict = {}
                late_members = []
                for member in card.members:
                    late_members.append(member.fullname)
                late_dict['members'] = late_members
                late_dict['title'] = card.name
                late_dict['description'] = card.desc
                late_dict['due'] = card._data['due'][:10]
                late_master.append(late_dict)

    data['late_stories'] = late_master    

    return render(request, 'index.html', data)