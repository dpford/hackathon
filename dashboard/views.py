from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from trollop import TrelloConnection

@never_cache
def home(request):
	data = {}
	conn = TrelloConnection('8e08cc15f33eba483bc2ec18f5d9d2e8', '546c06039131159676b3f7c41c295e6cb0529417861c27f0287122ceadcf3065')
	hackathon = conn.me.boards[4]
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

	return render(request, 'index.html', data)