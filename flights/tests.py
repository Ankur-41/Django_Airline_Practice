from django.db.models import Max
from django.test import Client,TestCase
from .models import Airport,Flight,Passenger

# Create your tests here.
class FlightTestCase(TestCase):
    def setUp(self):
        # create airports
        a1 = Airport.objects.create(code='AAA',city='City A')
        a2 = Airport.objects.create(code='BBB',city='City B')
        # create flight
        Flight.objects.create(origin=a1,destination=a2,duration=100)
        Flight.objects.create(origin=a1,destination=a1,duration=100)
        Flight.objects.create(origin=a1,destination=a2,duration=-100)

    def test_departure_count(self):
        a = Airport.objects.get(code='AAA')
        self.assertEqual(a.departures.count(),3)
    def test_arrival_count(self):
        a = Airport.objects.get(code='AAA')
        self.assertEqual(a.arrivals.count(),1)
    def test_invalid_flight(self):
        a1 = Airport.objects.get(code='AAA')
        a2 = Airport.objects.get(code='BBB')
        f = Flight.objects.get(origin=a1,destination=a1,duration=100)
        self.assertTrue(f.is_valid_flight())
    def test_index(self):
        c = Client()
        response = c.get('/flights/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['flights'].count(),3)
    def test_valid_flight(self):
        a1 = Airport.objects.get(code='AAA')
        a2 = Airport.objects.get(code='BBB')
        f = Flight.objects.get(origin=a1,destination=a2,duration=100)
        c = Client()
        response = c.get(f'/flights/result/{f.id}')
        self.assertEqual(response.status_code,200)
    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max('id'))['id__max']
        c = Client()
        response = c.get(f'flights/result/{max_id + 1}')
        self.assertEqual(response.status_code,404)
    def test_flight_passenger(self):
        f = Flight.objects.get(id=1)
        p = Passenger.objects.create(first_name='Chedi',last_name='Chapat')
        f.passengers.add(p)
        c = Client()
        response = c.get(f'/flights/result/{f.id}')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['passengers'].count(),1)
    def test_flight_non_passenger(self):
        f = Flight.objects.get(id=1)
        p = Passenger.objects.create(first_name='Chedi',last_name='Chapati')
        c = Client()
        response = c.get(f'/flights/result/{f.id}')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['passengers'].count(),0)


