from django.shortcuts import render
from models import Records, Taskinstances, Labellog
import random
import re
import json
import cameo
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):
    # load the json data
    event = get_random_instance(request)
    user_label_count, remaind_count = get_usr_label_count(request)
    event["user_label_count"] = user_label_count
    event["remaind_count"] = remaind_count

    return render(request, "tagging/tagging.html", event)

@login_required
def label(request):
    if request.method == "GET":
        flag = request.GET["flag"]
        label_instance_id = request.GET["label_instance_id"]

        # save the label data
        if flag != "0":
            instance = Taskinstances.objects.get(instance_id=label_instance_id)
            instance.status = flag
            instance.save()

            # write label log
            tagLog = Labellog(instance_id=label_instance_id, event_id=instance.event_id, 
                user_id=request.user.id, datetime=timezone.now(), flag=flag)
            tagLog.save()

    # return another random records
    event = get_random_instance(request)
    user_label_count, remaind_count = get_usr_label_count(request)
    event["user_label_count"] = user_label_count
    event["remaind_count"] = remaind_count

    return JsonResponse(event)

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'tagging/login.html', {})

def get_usr_label_count(request):
    user_id = request.user.id
    user_label_count = len(Labellog.objects.filter(user_id=user_id))
    remaind_count = len(Taskinstances.objects.filter(status='0'))
    return user_label_count, remaind_count

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("reg_username")
        passwd = request.POST.get("reg_password")
        email = request.POST.get("reg_email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        user = User.objects.create_user(username, email, passwd)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        new_user = authenticate(username=username, password=passwd)
        login(request, new_user)
        return HttpResponseRedirect("/tagging/")

def get_random_instance(request):
    text2code = cameo.text2code
    code2text = {v:k for k,v in text2code.items()}
    code2root = cameo.root2code

    user_id = request.user.id
    # find the labeled events
    labeled_events = {}
    for elog in Labellog.objects.filter(user_id=user_id):
        labeled_events[elog.event_id] = 1

    # find the available instances
    instances = []
    for ins in Taskinstances.objects.filter(status='0'):
        if ins.event_id not in labeled_events:
            instances.append(ins)
    if len(instances) == 0:
        return {"finished": True}
    # randomly choose a instance
    choosen_instance = random.choice(instances)

    record = Records.objects.get(event_id=choosen_instance.event_id)
    location = record.location.strip()
    loc_items = []
    if location and location != "":
        loc_items = location.split(",")

    record_content = record.content
    for loc_it in loc_items:
        record_content = re.sub(loc_it, "<mark>%s</mark>" % loc_it, record_content)

    paragraphs = re.split(r"\n+", record_content)
    eventType = code2root.get(record.event_type, record.event_type)
    subType = code2text.get(record.event_subtype, eventType)
    eventId = record.event_id

    event = {"finished":False,"eventId": eventId, "instanceId": choosen_instance.instance_id, "location": record.location, "eventType": eventType,
    "ps": paragraphs, "subType": subType, "actor1": record.actor1, "actor2": record.actor2, "date":record.event_date, "title": record.title}
    return event

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        passwd = request.POST.get("password")
        user = authenticate(username=username, password=passwd)

        if user:
            if user.is_active:
                login(request, user)
                event = get_random_instance(request)
                return HttpResponseRedirect("/tagging/")
            else:
                return render(request, 'tagging/login.html', {"login_error_msg": "Your account is disabled."})
        else:
            return render(request, 'tagging/login.html', {"login_error_msg": "The login credentials you entered do not match our records."})
    else:
        return render(request, 'tagging/login.html', {})

def check_user(request):
    if request.method == "GET":
        username = request.GET.get("reg_username")
        try:
            User.objects.get(username=username)
            return JsonResponse({"code":1, "message":u"Username <code>%s</code> is already in use." % username})
        except User.DoesNotExist:
            return JsonResponse({"code":0, "message":"ok"})
