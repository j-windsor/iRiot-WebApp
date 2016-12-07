from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Device, Function
from rooms.models import Room
import boto3
import json
import re
from random import randint

# Create your views here.
@login_required
def new(request):
    d = Device()
    d.name = request.POST['name']
    d.room = Room.objects.get(id=request.POST['room_id'])
    d.save()
    for key in request.POST.keys():
        if key[:2] == 'nf':
            make_function(request, request.POST["nf"+key[2:]],request.POST["np"+key[2:]],-1,d)

    return HttpResponseRedirect('/devices/'+request.POST['room_id']+'/manage')

@login_required
def update(request):
    dev = Device.objects.get(id=request.POST['device_id'])
    if dev.room.owner != request.user:
        messages.warning(request, "You can't update a device you dont own!")
        return HttpResponseRedirect('/devices/'+request.POST['room_id']+'/manage')
    dev.name = request.POST['q']
    dev.save()

    #modify existing fields
    for key in request.POST.keys():
        if key[0] == 'f':
            make_function(request, request.POST["f"+key[1:]],request.POST["p"+key[1:]],key[1:])
        if key[:2] == 'nf':
            make_function(request, request.POST["nf"+key[2:]],request.POST["np"+key[2:]],-1,dev)

    return HttpResponseRedirect('/devices/'+request.POST['room_id']+'/manage')

@login_required
def make_function(request, name, code, existing_id, d=None):
    f = Function()
    if existing_id != -1:
        f = Function.objects.get(id=existing_id)
    f.function = name
    hexstring = code.replace("0x","").replace(" ","").replace(",","").upper()
    if re.match("^[0-9A-F]+$", hexstring) and len(hexstring) % 4 == 0:
        hexarray = [hexstring[i:i+4] for i in range(0, len(hexstring), 4)]
        f.prontohex = " ".join(hexarray)
        sendhexstring = ""
        for s in hexarray:
            sendhexstring += str(int(s, 16)) + ","
        f.sendhex = sendhexstring[:-1]
        if existing_id == -1:
            f.device = d
        f.save()
    else:
        messages.warning(request, "ProntoHex code invalid for " + name)
        if existing_id == -1:
            for code in d.function_set.all():
                code.delete()
            d.delete()
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
    #delete all prontohex codes associated with device
    for code in dev.function_set.all():
        code.delete()
    dev.delete()
    return HttpResponseRedirect('/devices/'+str(room_id)+'/manage')

@login_required
def send_function(request, function_id):
    client = boto3.client('iot-data', region_name='us-east-1')
    func = Function.objects.get(id=function_id)
    payload = {"state":{"desired":{"prontohex": func.sendhex+"d"+str(randint(1,99))}}}
    if func.device.room.owner != request.user:
        HttpResponse("f")
    try:
        for hub in func.device.room.hub_set.all():
            client.update_thing_shadow(thingName=hub.serial_number,payload=json.dumps(payload))
    except:
        return HttpResponse("f")
    return HttpResponse("t")
