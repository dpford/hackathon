from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

def home(request):
	return render(request, 'index.html', [])