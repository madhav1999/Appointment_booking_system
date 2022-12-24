from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Booktime, datalist
from collections import defaultdict
import datetime
from datetime import timedelta
from . import forms
from django.core.exceptions import FieldError

Choicefieldfromhere = []


def seebookinformation(request):
    coaches = datalist.objects.all()
    result = {}
    totalslots = {}
    remainingtimeslots = {}
    for i in coaches:
        coach = datalist.objects.filter(id=i.id)
        slottimes = Booktime.objects.filter(CoachName__in=coach)
        totalslots[i.id] = len(slottimes)
        result[i.id] = slottimes
        # print(datalist.objects.get(id=i.id).TotalSlotFrom -
        #   datalist.objects.get(id=i.id).TotalSlotuntil)
        time1 = datetime.datetime.strptime(
            str(datalist.objects.get(id=i.id).TotalSlotFrom), '%H:%M:%S')
        time2 = datetime.datetime.strptime(
            str(datalist.objects.get(id=i.id).TotalSlotuntil), '%H:%M:%S')
        difference = time2-time1
        remainingtimeslots[i.id] = (
            ((difference.seconds)//60) // 30)-totalslots[i.id]

    # print(result)
    context = {}
    context['coaches'] = coaches
    context['filled'] = result
    context['totalslots'] = totalslots
    context['remainingtimeslots'] = remainingtimeslots

    return render(request, 'data/index.html', context)


def insertview(request, id):
    time1 = datetime.datetime.strptime(
        str(datalist.objects.get(id=id).TotalSlotFrom), '%H:%M:%S')
    time2 = datetime.datetime.strptime(
        str(datalist.objects.get(id=id).TotalSlotuntil), '%H:%M:%S')
    offset = timedelta(minutes=30)
    resultset = []
    alreadythere = []
    coaches = datalist.objects.all()
    time1 = time1 - offset
    start = time1
    end = time2 - offset
    print("start ------------>", start)

    coach = datalist.objects.filter(id=id)
    slottimes = Booktime.objects.filter(CoachName__in=coach)
    for j in slottimes:
        alreadythere.append(j.Slotperiodfrom)

    while (time1 <= start and end > start):
        start = start+offset
        resultset.append(start.time())

    Finaltimings = []
    for i in resultset:
        if not i in alreadythere:
            Finaltimings.append(i)
    global Choices
    Choices = []
    for i in Finaltimings:
        Choices.append((i, i))
    print(Choices)

    slot_choices = [(1, 1)]
    obj = datalist.objects.get(id=id)
    if request.method == 'POST':
        form = forms.insertform(request.POST)
        form.fields['Slotperiodfrom'].choices = Choices

        if form.is_valid():
            if Booktime.objects.filter(CoachName=obj, Slotperiodfrom=request.POST['Slotperiodfrom']).exists():
                return render(request, "data/error.html", {'alreadybook': 1})
            timeobj = datalist.objects.get(id=id)
            starttime = timeobj.TotalSlotFrom
            endtime = timeobj.TotalSlotuntil
            submittime = datetime.datetime.strptime(
                request.POST['Slotperiodfrom'], '%H:%M:%S').time()

            if not starttime <= submittime and submittime <= endtime:
                return render(request, "data/error.html", {'limit': 1})

            form.save()
            return HttpResponseRedirect("/get")

    if len(Finaltimings) == 0:
        return render(request, "data/error.html", {'Noslots': 1, 'coach': coach})
    form = forms.insertform(initial={'CoachName': obj})
    form.fields['Slotperiodfrom'].choices = Choices

    context = {}
    context['form'] = form

    return render(request, 'data/insert.html', context)


def deleteview(request, id):
    context = {}
    obj = get_object_or_404(Booktime, id=id)
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect("/get")
    return render(request, 'data/deleteview.html', context)


def detailstodeleteslot(request):
    coaches = datalist.objects.all().order_by('Day')
    result = {}
    totalslots = {}
    remainingtimeslots = {}
    for i in coaches:
        coach = datalist.objects.filter(id=i.id)
        slottimes = Booktime.objects.filter(CoachName__in=coach)
        totalslots[i.id] = len(slottimes)
        result[i.id] = slottimes
        # print(datalist.objects.get(id=i.id).TotalSlotFrom -
        #   datalist.objects.get(id=i.id).TotalSlotuntil)
        time1 = datetime.datetime.strptime(
            str(datalist.objects.get(id=i.id).TotalSlotFrom), '%H:%M:%S')
        time2 = datetime.datetime.strptime(
            str(datalist.objects.get(id=i.id).TotalSlotuntil), '%H:%M:%S')
        difference = time2-time1
        remainingtimeslots[i.id] = (
            ((difference.seconds)//60) // 30)-totalslots[i.id]

    # print(result)
    context = {}
    context['coaches'] = coaches
    context['filled'] = result
    context['totalslots'] = totalslots
    context['remainingtimeslots'] = remainingtimeslots
    print(context)

    return render(request, 'data/detailstodelete.html', context)


def mainpage(request):
    return render(request, 'data/mainpage.html')
