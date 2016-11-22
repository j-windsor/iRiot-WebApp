from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Hub
from rooms.models import Room
from .forms import HubForm
import boto3
import botocore

# Create your views here.
@login_required
def manage(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        client = boto3.client('iot', region_name='us-east-1')
        # create a form instance and populate it with data from the request:
        f = HubForm(request.POST)
        # check whether it's valid:
        if f.is_valid():
            # Save the form data to the database.
            # But dont yet commit, we still have some data to add.
            hub = f.save(commit=False)
            isTaken = True
            try:
                isTaken = client.describe_thing(thingName=hub.serial_number)['attributes']['taken'] == 'true'
            except botocore.exceptions.ClientError:
                messages.warning(request, 'There is no device with that serial number!')
                return render(request, 'hubs/manage.html', {'hub_form': f})
            except:
                messages.warning(request, 'Error communicating with device!')
                return render(request, 'hubs/manage.html', {'hub_form': f})
            if isTaken:
                messages.warning(request, 'Hub Already Registered!')
                return render(request, 'hubs/manage.html', {'hub_form': f})

            hub.owner = request.user

            client.update_thing(thingName=hub.serial_number,attributePayload={'attributes': {'taken': 'true'},'merge': True})

            # NOW we can save
            hub.save();




            # redirect to a new URL:
            return HttpResponseRedirect('/hubs/manage')
        else:
            messages.warning(request, "There were some errors in your request. Try Again!")
            return render(request, 'hubs/manage.html', {'hub_form': f})
    # if a GET (or any other method) we'll create a blank form
    else:
        hub_form = HubForm()
        return render(request, 'hubs/manage.html', {'hub_form': hub_form})

    return render(request, 'hubs/master.html')

@login_required
def remove_hub(request, hub_id):
    client = boto3.client('iot', region_name='us-east-1')
    hub = Hub.objects.get(id=hub_id)
    if hub.owner == request.user:
        try:
            client.update_thing(thingName=hub.serial_number,attributePayload={'attributes': {'taken': 'false'},'merge': True})
        except:
            messages.warning(request, "Hub could not be removed. Communication with device failed.")
            return HttpResponseRedirect('/hubs/manage')

        hub.delete()
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
