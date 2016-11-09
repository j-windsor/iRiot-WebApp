from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Device, Function
from rooms.models import Room
import boto3
import json

# Create your views here.
@login_required
def new(request):
    d = Device()
    d.name = request.POST['name']
    d.room = Room.objects.get(id=request.POST['room_id'])
    d.save()
    messages.warning(request, request.POST.keys())
    for key in request.POST.keys():
        if key[:2] == 'nf':
            f = Function()
            f.function = request.POST["nf"+key[2:]]
            f.prontohex = request.POST["np"+key[2:]]
            f.device = d
            f.save()

    return HttpResponseRedirect('/devices/'+request.POST['room_id']+'/manage')

@login_required
def update(request):
    dev = Device.objects.get(id=request.POST['device_id'])
    if dev.room.owner != request.user:
        messages.warning(request, "You can't update a device you dont own!.")
        return HttpResponseRedirect('/devices/'+request.POST['room_id']+'/manage')
    dev.name = request.POST['q']
    dev.save()

    #modify existing fields
    for key in request.POST.keys():
        if key[0] == 'f':
            func = Function.objects.get(id=key[1:])
            func.function = request.POST[str("f"+key[1:])]
            func.prontohex = request.POST[str("p"+key[1:])]
            func.save()
        if key[:2] == 'nf':
            f = Function()
            f.function = request.POST["nf"+key[2:]]
            f.prontohex = request.POST["np"+key[2:]]
            f.device = dev
            f.save()

    return HttpResponseRedirect('/devices/'+request.POST['room_id']+'/manage')


@login_required
def manage(request, room_id):
    if Room.objects.get(id=room_id).owner != request.user:
        messages.warning(request, "You can't manage a device you dont own.")
        return HttpResponseRedirect("/")
    name = Room.objects.get(id=room_id).name
    return render(request, 'devices/manage.html', {'roomDevices': Device.objects.filter(room__id=room_id), 'roomID': room_id, 'roomName': name})

@login_required
def remove_device(request, device_id, room_id):
    dev = Device.objects.get(id=device_id)
    if dev.room.owner != request.user:
        messages.warning(request, "Your device was not removed.")
        return HttpResponseRedirect('/devices/'+str(room_id)+'/manage')
    dev.delete()
    return HttpResponseRedirect('/devices/'+str(room_id)+'/manage')

def send_function(request, function_id):
    client = boto3.client('iot-data', region_name='us-east-1')
    func = Function.objects.get(id=function_id)
    payload = {"state":{"desired":{"prontohex": func.prontohex}}}
    if func.device.room.owner != request.user:
        HttpResponse("f")
    try:
        for hub in func.device.room.hub_set.all():
            client.update_thing_shadow(thingName=hub.serial_number,payload=json.dumps(payload))
    except:
        return HttpResponse("f")
    return HttpResponse("t")
