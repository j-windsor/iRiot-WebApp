from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Hub
from rooms.models import Room
from .forms import HubForm

# Create your views here.
@login_required
def manage(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        f = HubForm(request.POST)
        # check whether it's valid:
        if f.is_valid():
            # Save the form data to the database.
            # But dont yet commit, we still have some data to add.
            hub = f.save(commit=False)
            hub.owner = request.user
            #TODO: Check to see if hub is in AWS and not taken
            # NOW we can save
            hub.save();

            # redirect to a new URL:
            return HttpResponseRedirect('/hubs/manage')
        else:
            messages.warning(request, 'Hub Not Added!')
            return render(request, 'hubs/manage.html', {'hub_form': f})
    # if a GET (or any other method) we'll create a blank form
    else:
        hub_form = HubForm()
        return render(request, 'hubs/manage.html', {'hub_form': hub_form})

    return render(request, 'hubs/master.html')

@login_required
def remove_hub(request, hub_id):
    if Hub.objects.filter(owner=request.user):
        Hub.objects.get(id=hub_id).delete()
    else:
        messages.warning(request, "Your hub was not deleted.")
    return HttpResponseRedirect('/hubs/manage')

@login_required
def change_name(request):
    item = Hub.objects.get(id=request.POST["hub_id"])
    if item.owner == request.user:
        item.alias = request.POST['q']
        item.save()
    else:
        messages.warning(request, 'Name not changed!')
    return HttpResponseRedirect('/hubs/manage')

@login_required
def change_room(request):
    item = Hub.objects.get(id=request.POST["hub_id"])
    room = Room.objects.get(id=request.POST["room_val"])
    if item.owner == request.user:
        item.room = room
        item.save()
    else:
        messages.warning(request, 'Name not changed!')
    return HttpResponseRedirect('/hubs/manage')
