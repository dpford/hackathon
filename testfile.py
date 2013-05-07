from trollop import TrelloConnection
import datetime

conn = TrelloConnection('69387d468622b15d7a0a571e8165a793', 'c2021799351a98257f7cfde07b51d599434794eecf02c4923515769d0a5bbefc')

print conn

print conn.me

print "Show boards"
print conn.me.boards

print "Get Hackathon board"
hackathon = conn.me.boards[0]
print conn.me.boards[0]

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

# Create an empty dict for each category
    
mem_categories = {}
for list in hackathon.lists:
    mem_categories[list.name] = 0
print mem_categories



print "Create a dict entry for each member"
adv_mem_count = {}
for member in board_members:
	adv_mem_count[member.fullname] = mem_categories.copy()

print adv_mem_count

print "Populate dict"
for card in hackathon.cards:
	for member in card.members:
		adv_mem_count[member.fullname][card.list.name] += 1

print adv_mem_count
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
            
for key in list_count:
    print key
for key, value in adv_mem_count.items():
    print key
    for key2, value2 in value.items():
        print value2
    