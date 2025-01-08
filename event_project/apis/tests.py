from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from .models import Event 
from datetime import timedelta

class UserAPITestCase(APITestCase):
    def test_register_user(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        # First, create a user
        self.client.post('/api/users/register/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        })

        # Then, attempt to log in
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_user(self):
        # First, create and log in a user
        self.client.post('/api/users/register/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        })

        login_response = self.client.post('/api/users/login/', {
            "username": "testuser",
            "password": "password123"
        })
        token = login_response.data['token']

        # Set the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Log out the user
        response = self.client.get('/api/users/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EventAPITestCase(APITestCase):
    def setUp(self):
        # Create two users: one will be the owner of the event and the other will not
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="testpassword")
        future_date = now() + timedelta(days=1)

        # Create an event for the 'testuser' (owner)
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            date=future_date,
            location="Test Location",
            ticket_price=100.0,
            organizer=self.user  # Set the user who created the event
        )
        
        # Create a token for the user and set authorization header for 'testuser'
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_events(self):
        response = self.client.get('/api/events/list-events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['events']), 1)

    def test_list_upcoming_events(self):
        response = self.client.get('/api/events/upcoming/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['events']), 0)

    def test_create_event(self):
        response = self.client.post('/api/events/create-event/', {
            'title': 'New Event',
            'description': 'This is a new event.',
            'date': now().isoformat(),
            'location': 'New Location',
            'ticket_price': 50.0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['event']['title'], 'New Event')

    def test_retrieve_event(self):
        response = self.client.get(f'/api/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.event.title)

    def test_update_event_by_owner(self):
        # The owner updates the event
        response = self.client.put(f'/api/events/{self.event.id}/edit/', {
            'title': 'Updated Event',
            'description': 'Updated description.',
            'date': now().isoformat(),
            'location': 'Updated Location',
            'ticket_price': 150.0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event']['title'], 'Updated Event')

    def test_update_event_by_non_owner(self):
        # Log in as the other user who did not create the event
        self.client.logout()
        self.token = Token.objects.create(user=self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Try to update the event created by 'testuser'
        response = self.client.put(f'/api/events/{self.event.id}/edit/', {
            'title': 'Updated Event',
            'description': 'Updated description.',
            'date': now().isoformat(),
            'location': 'Updated Location',
            'ticket_price': 150.0
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_by_owner(self):
        # The owner deletes the event
        response = self.client.delete(f'/api/events/{self.event.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_by_non_owner(self):
        # Log in as the other user who did not create the event
        self.client.logout()
        self.token = Token.objects.create(user=self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Try to delete the event created by 'testuser'
        response = self.client.delete(f'/api/events/{self.event.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_no_events(self):
        Event.objects.all().delete()
        response = self.client.get('/api/events/list-events/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Message', response.data)