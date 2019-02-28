from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse('Hi you\'re at bbapp index')


def player_page(request, player_id):
    return HttpResponse(f"player page {player_id}")


def pitching(request, player_id):
    return HttpResponse(f"pitching page for player {player_id}")


def batting(request, player_id):
    return HttpResponse(f"batting page for player {player_id}")
