from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'belt/index.html')

def travels(request):
    if 'userid' not in request.session:
        return redirect ("/")
    context = {
        'user' : User.objects.get(id=request.session['userid']),
        'mytrips' : Trip.objects.all(),
        'other_trips' : Trip.objects.all().exclude(id=request.session['userid'])
    }
    print context['user'].name
    # print context['mytrips'].trip_location
    return render(request, 'belt/travel_dashboard.html', context)

def itinerary(request, id):
    if 'userid' not in request.session:
        return redirect ("/")
    context = {
        "id": id,
        'trip_details' : Trip.objects.get(id=id),
    }
    return render(request, 'belt/itinerary.html', context)

def add_trip(request):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['userid'])
    }
    return render(request, 'belt/add_trip.html', context)

def process_trip(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        newtrip= Trip.objects.trip_validate(request.POST, request.session['userid'])
        print newtrip
        if newtrip[0] == False:
            for each in newtrip[1]:
                messages.add_message(request, messages.INFO, each)
        if newtrip[0] == True:
            messages.add_message(request, messages.INFO, "Trip Added")
            return redirect('/travels')


def delete(request, id):
    # try:
    #     target = Trip.objects.get(id=id)
    # except Trip.DoesNotExist:
    #     messages.add_message(request, messages.INFO, "Not allowed")
    #     return redirect('/travels')
    Trip.objects.get(id=id).delete()
    return redirect('/travels')

def register(request):
    if request.method == 'GET':
        return redirect ('/')
    newuser = User.objects.validate(request.POST)
    print newuser
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each)
        return redirect('/')
    if newuser[0] == True:
        messages.success(request, 'Well done')
        request.session['userid'] = newuser[1].id
        return redirect('/travels')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.login(request.POST)
        print user
        if user[0] == False:
            for each in user[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('/')
        if user[0] == True:
            messages.add_message(request, messages.INFO,'Welcome, You are logged in!')
            request.session['userid'] = user[1].id
            return redirect('/travels')

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    print "*******"
    print request.session['userid']
    del request.session['userid']
    return redirect('/')
