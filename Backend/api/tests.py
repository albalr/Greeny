"""
This module contains unit tests for the Greeny application.

It includes tests for the Statistics functionality, and for the 
FetchPublicTransportStations methods.
"""
# Standard library imports
import json
import os
from unittest.mock import patch

# Third-party imports
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import PublicTransportStation, Station, Statistics, Stop, TransportType, User, Route
from .utils import calculate_co2_consumed, calculate_car_co2_consumed
from rest_framework.test import APIRequestFactory, force_authenticate

# Local application/library specific imports
from api.friend_view import FriendViewSet, FriendRequestViewSet
from .models import (User, FriendRequest, Station, PublicTransportStation,
                     Stop, TransportType, Statistics)


class FetchPublicTransportStationsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("fetch_all_stations")  # replace with the actual URL name for the view

    def test_get(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.redirect_chain[0][0], '/api/bus-stops')
        self.assertEqual(response.redirect_chain[0][1], 302)

        self.assertEqual(response.redirect_chain[1][0], '/api/bicing')
        self.assertEqual(response.redirect_chain[1][1], 302)

        self.assertEqual(response.redirect_chain[2][0], '/api/charging-points')
        self.assertEqual(response.redirect_chain[2][1], 302)

    @patch('requests.get')
    def test_parse_api_data(self, mock_get):

        mock_get.return_value.status_code = 200

        script_dir = os.path.dirname(__file__)

        json_file_path = os.path.join(script_dir, 'fixtures', 'mock_api.json')

        # Read the mock data from the json file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            mock_data = json.load(file)

        mock_get.return_value.json.return_value = mock_data

        response = self.client.get(self.url, follow=False)

        self.assertEqual(response.status_code, 302)

        # Check that the data has been parsed correctly
        # Replace 'key1' and 'key2' with the actual keys in the response data
        self.assertEqual(Station.objects.count(), 1)
        self.assertEqual(PublicTransportStation.objects.count(), 1)

        station = Station.objects.get(name__iexact='Catalunya')
        t_type = TransportType.objects.get(type=TransportType.TTransport.METRO)
        self.assertEqual(Stop.objects.filter(station=station).count(), 3)
        self.assertEqual(len(Stop.objects.get(station=station, transport_type=t_type).lines), 2)

class FinalFormTransports(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_post_success(self):
        data = {
            'selectedTransports': ['Walking', 'Bus', 'Bike'],
            'totalDistance': 100,
            'startedAt': '2024-04-25T16:33:14.90961'
        }
        response = self.client.post(reverse('final_form_transports'), data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Route.objects.count(), 1)
        self.assertEqual(Statistics.objects.count(), 1)

    def test_data_statistics(self):
        data = {
            'selectedTransports': ['Walking', 'Bus', 'Bike', 'Motorcycle'],
            'totalDistance': 100,
            'startedAt': '2024-04-25T16:33:14.90961'
        }

        response = self.client.post(reverse('final_form_transports'), data=json.dumps(data), content_type='application/json')


        self.assertEqual(Statistics.objects.count(), 1)
        self.assertEqual(Statistics.objects.get().km_Walked, 25)
        self.assertEqual(Statistics.objects.get().km_Bus, 25)
        self.assertEqual(Statistics.objects.get().km_Biked, 25)
        self.assertEqual(Statistics.objects.get().km_Motorcycle, 25)

    def test_statics_km_totals(self):
        data = {
            'selectedTransports': ['Walking', 'Bus', 'Bike'],
            'totalDistance': 100,
            'startedAt': '2024-04-25T16:33:14.90961'
        }

        response = self.client.post(reverse('final_form_transports'), data=json.dumps(data), content_type='application/json')


        self.assertEqual(Statistics.objects.count(), 1)
        self.assertEqual(Statistics.objects.get().km_Totals, 100)

    def test_two_routes(self):
        data = {
            'selectedTransports': ['Walking', 'Bus'],
            'totalDistance': 150.70,
            'startedAt': '2024-04-25T16:33:14.90961'
        }

        response = self.client.post(reverse('final_form_transports'), data=json.dumps(data), content_type='application/json')


        self.assertEqual(Route.objects.count(), 1)
        self.assertEqual(Statistics.objects.count(), 1)

        request = self.client.post(reverse('final_form_transports'), data=json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.user)
        response = self.client.post(request)

        self.assertEqual(Route.objects.count(), 2)
        self.assertEqual(Statistics.objects.count(), 1)

    def test_not_answering_form(self):
        data = {
            'selectedTransports': [],
            'totalDistance': 100,
            'startedAt': '2024-04-25T16:33:14.90961'
        }

        response = self.client.post(reverse('final_form_transports'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(Statistics.objects.count(), 1)
        self.assertEqual(Statistics.objects.get().km_Walked, 0)
        self.assertEqual(Statistics.objects.get().km_Bus, 0)
        self.assertEqual(Statistics.objects.get().km_Biked, 0)
        self.assertEqual(Statistics.objects.get().km_Motorcycle, 0)
        self.assertEqual(Statistics.objects.get().km_Car, 0)
        self.assertEqual(Statistics.objects.get().km_PublicTransport, 0)
        self.assertEqual(Statistics.objects.get().km_ElectricCar, 0)
        self.assertEqual(Statistics.objects.get().km_Totals, 0)
        self.assertEqual(Route.objects.count(), 1)

    def test_co2_consumed(self):
        data = {
            'selectedTransports': ['Bus'],
            'totalDistance': 100,
            'startedAt': '2024-04-25T16:33:14.90961'
        }

        response = self.client.post(reverse('final_form_transports'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(Statistics.objects.count(), 1)
        self.assertEqual(Statistics.objects.get().kg_CO2_consumed, 0.08074 * 100)
        self.assertEqual(Statistics.objects.get().kg_CO2_car_consumed, 0.143 * 100)
        self.assertEqual(Route.objects.count(), 1)
        self.assertEqual(Route.objects.get().consumed_co2, 0.08074 * 100)
        self.assertEqual(Route.objects.get().car_consumed_co2, 0.143 * 100)

    def test_calculate_co2_consumed(self):
        self.assertAlmostEqual(calculate_co2_consumed(['Walking', 'Walking'], 10), 0.0)
        self.assertAlmostEqual(calculate_co2_consumed(['Bike', 'Bike', 'Bike'], 20), 0.0)
        self.assertAlmostEqual(calculate_co2_consumed(['Bus'], 15), 0.08074 * 15)
        self.assertAlmostEqual(calculate_co2_consumed(['Car'], 25), 0.143 * 25)
        self.assertAlmostEqual(calculate_co2_consumed(['Electric Car'], 30), 0.070 * 30)
        self.assertAlmostEqual(calculate_co2_consumed(['Metro', 'Metro'], 40), 0.05013 * 20 + 0.05013 * 20)

    def test_calculate_car_co2_consumed(self):
        self.assertAlmostEqual(calculate_car_co2_consumed(20), 0.143 * 20)
        self.assertAlmostEqual(calculate_car_co2_consumed(30), 0.143 * 30)
        self.assertAlmostEqual(calculate_car_co2_consumed(40), 0.143 * 40)




class FriendRequestViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser', email='testuser@mail.com')
        self.friend = User.objects.create(username='friend', email='uwu@mail.com')
        self.FriendRequest = FriendRequest.objects.create(from_user=self.friend, to_user=self.user)

    def test_create_friend_request(self):
        request = self.factory.post('/friend-requests/', {'to_user': self.friend.id})
        force_authenticate(request, user=self.user)
        view = FriendRequestViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_list_friend_requests(self):
        request = self.factory.get('/friend-requests/')
        force_authenticate(request, user=self.user)
        view = FriendRequestViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_accept_friend_request(self):
        request = self.factory.delete(f'/friend-requests/{self.FriendRequest.id}/')
        force_authenticate(request, user=self.user)
        view = FriendRequestViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.FriendRequest.id)
        self.assertEqual(response.status_code, 200)

class FriendViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser', email='testuser@mail.com')
        self.friend = User.objects.create(username='friend', email='uwu@mail.com')
        self.user.friends.add(self.friend)

    def test_list_friends(self):
        request = self.factory.get('/friends/')
        force_authenticate(request, user=self.user)
        view = FriendViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

class UsersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_get_queryset(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_create_user(self):
        data = {
            "username": "testuser2",
            "password": "testpass2"
        }
        response = self.client.post('/api/user/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='testuser2').username, 'testuser2')