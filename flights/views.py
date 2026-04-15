from django import forms
from .models import Airport,Flight,Passenger
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import FlightDetails,SearchDetails,PassengerForm

# Create your views here only.

def index(request):
    flights = Flight.objects.all()
    return render(request,'flights/index.html',{
        'flights' : flights
    })

def search(request):
    if request.method == 'POST':
        form = SearchDetails(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                flight = Flight.objects.get(id=data['flight_id'])
                return render(request,'flights/results.html',{
                    'flight' : flight,
                    'passengers' : flight.passengers.all(),
                    'non_passengers' : Passenger.objects.exclude(flights = flight).all()
                })
            except Flight.DoesNotExist:
                return render(request,'flights/results.html',{
                    'flight' : None,
                    'passengers' : [] 
                })
        return render(request,'flights/search.html',{
            'form' : form
        })
    return render(request,'flights/search.html',{
        'form' : SearchDetails()
    })

def add(request):
    if request.method == 'POST':
        flight_form = FlightDetails(request.POST)
        if flight_form.is_valid():
            user_data = flight_form.cleaned_data

            origin,_ = Airport.objects.get_or_create(
                code = user_data['origin_code'],
                defaults= {'city' : user_data['origin_city']}
            )

            destination,_ = Airport.objects.get_or_create(
                code = user_data['destination_code'],
                defaults= {'city' : user_data['destination_city']}
            )

            flight = Flight(
                origin = origin,
                destination = destination,
                duration = user_data['duration']
            )
            if flight.is_valid_flight():
                flight.save()
                return HttpResponseRedirect(reverse('flights:index'))
            else:
                return render(request,'flights/add.html',{
                    'form' : flight_form,
                    'error' : 'Invalid Flight Details'
                })
    
        else:
            return render(request,'flights/add.html',{
                'form' : flight_form
            })

    return render(request,'flights/add.html',{
            'form' : FlightDetails()
        })

def add_passenger(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('flights:index'))
        else:
            return render(request,'flights/addpassenger.html',{
                'form' : form
            })
    return render(request,'flights/addpassenger.html',{
            'form' : PassengerForm()
        })


def result(request,flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
        return render(request,'flights/results.html',{
            'flight' : flight,
            'passengers' : flight.passengers.all(),
            'non_passengers' : Passenger.objects.exclude(flights = flight).all()
        })
    except Flight.DoesNotExist:
        return render(request,'flights/results.html',{
            'flight' : None,
            'passengers' : [] 
        })

def book(request,flight_id):
    if request.method == 'POST':
        flight = Flight.objects.get(id = flight_id)
        passenger = Passenger.objects.get(id = int(request.POST['passenger']))
        passenger.flights.add(flight)
    return HttpResponseRedirect(reverse('flights:result',args=[flight_id]))


