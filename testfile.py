from trollop import TrelloConnection

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

