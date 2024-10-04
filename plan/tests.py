from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from .models import Plan

class VoteAPlanTestCase(APITestCase):
    def setUp(self):
        self.plan = Plan.objects.create(title="test plan", body="test plan body")
        self.url = reverse('vote_a_plan', kwargs={'plan_id': self.plan.id})
        self.users = []
        for i in range(6):
            user = User.objects.create_user(username=f'testuser{i}', password='password123')
            self.users.append(user)

    def authenticate_user(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

    def test_successful_vote_submission(self):
        """Test successful vote submition"""
        user = self.users[0]
        self.authenticate_user(user)
        data = {'vote': 5}
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Vote successfully submitted.')

    def test_invalid_vote_submission(self):
        """Test can not vote with invalid data"""
        user = self.users[0]
        self.authenticate_user(user)
        data = {}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('vote', response.data)

    def test_high_vote_throttling(self):
        """Test throttle error for high vote numbers"""
        for i in range(6):
            user = self.users[i]
            self.authenticate_user(user)
            data = {'vote': 5}
            
            response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        
    def test_low_vote_throttling(self):
        """Test throttle error for low vote numbers"""
        for i in range(6):
            user = self.users[i]
            self.authenticate_user(user)
            data = {'vote': 1}
            
            response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
