from django.shortcuts import render
from rooms.forms import RoomForm

# Create your views here.

def index(request):
    return render(request, 'master/index.html', {'room_form': RoomForm()})
