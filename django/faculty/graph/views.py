from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json
import time
import requests
from .models import Sensor


@login_required
def monitor(request):
    return render(request, 'graph/monitor.html')


@csrf_exempt
def node(request):
    x = (time.time() - time.timezone) * 1000
    try:
        # ip address of the common network in which the node and pc is running in
        response = requests.get("http://192.168.xx.xxx/Python")
    except:
        pass
    y = int(response.text)
    db = Sensor(data=y)
    db.save()
    return HttpResponse(json.dumps([x,y]), content_type="application/json")
