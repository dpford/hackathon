from trollop import TrelloConnection
import datetime

conn = TrelloConnection('8e08cc15f33eba483bc2ec18f5d9d2e8', '546c06039131159676b3f7c41c295e6cb0529417861c27f0287122ceadcf3065')

print conn

print conn.me

print "Show boards"
print conn.me.boards

print "Get Hackathon board"
hackathon = conn.me.boards[4]
print conn.me.boards[4]

print "Show cards"
print hackathon.cards

print "First card"
first_card = hackathon.cards[5]
print first_card

print "First card name"
print first_card.name

print "Card labels"
labels = first_card.labels
print labels

print "Card memebers"
members = first_card.members
print members

print "*** Get cards for member ***"
member_cards = hackathon.members[1].cards

print "*** Get member counts ***"
board_members = hackathon.members

print "Create a dict entry for each member"
mem_count = {}
for member in board_members:
	mem_count[member.fullname] = 0

print mem_count

print "Populate dict"
for card in hackathon.cards:
	for member in card.members:
		mem_count[member.fullname] += 1

print mem_count

print "Count of each list"
list_count = {}
for list in hackathon.lists:
    list_count[list.name] = len(list.cards)
    
print list_count

todaydate = datetime.datetime.now()
late_master = []
for card in hackathon.cards:
    if card._data['due']:
        duedate = datetime.datetime.strptime(card._data['due'][:19], '%Y-%m-%dT%H:%M:%S')
        if duedate < todaydate:
            late_dict = {}
            late_members = []
            for member in card.members:
                late_members.append(member.fullname)
            late_dict['members'] = late_members
            late_dict['title'] = card.name
            late_dict['description'] = card.desc
            late_dict['due'] = card._data['due'][:10]
            print late_dict
            late_master.append(late_dict)