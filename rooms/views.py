from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import RoomForm
from .models import Room
from devices.models import Device

# Create your views here.
@login_required
def room(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        f = RoomForm(request.POST)
        # check whether it's valid:
        if f.is_valid():
            # Save the form data to the database.
            # But dont yet commit, we still have some data to add.
            room = f.save(commit=False)
            room.owner = request.user
            # NOW we can save
            room.save();

            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Room Not Added!')
            return render(request, 'master/index.html', {'room_form': f})
    # if a GET (or any other method) we'll create a blank form
    else:
        room_form = RoomForm()
        return render(request, 'master/index.html', {'room_form': room_form})

    return render(request, 'master/index.html')

@login_required
def remove_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.owner == request.user:
        for device in room.device_set.all():
            device.delete()
        room.delete()
    else:
        messages.warning(request, "Your room was not removed.")
    return HttpResponseRedirect('/')

def edit_room_name(request):
    item = Room.objects.get(id=request.POST["room_id"])
    if item.owner == request.user:
        item.name = request.POST['q']
        item.save()
    else:
        messages.warning(request, 'Name not changed!')
    return HttpResponseRedirect('/')
