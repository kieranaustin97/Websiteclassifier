"""Django Views Test File"""
import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from classifier.models import PredictedWebsites
from django.contrib.auth import authenticate, login
#from classifier.view import index, showresults

class TestViews(TestCase):

    """Tests for Views"""
    def test_index_GET(self):
        
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

        responce = self.client.get(reverse('index'))

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/home.html')

    def test_index_POST(self):
        
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        responce = self.client.post(reverse('index'),{
            'url':'https://www.google.com'
        })

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/output.html')
        self.assertEqual(PredictedWebsites.objects.count(), 1)
        

    def test_showresults_empty_GET(self):
        
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

        responce = self.client.get(reverse('showresults'))

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/noResults.html')
        self.assertEqual(PredictedWebsites.objects.count(), 0)

    def test_showresults_GET(self):
        
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

        PredictedWebsites.objects.create(
            url="https://www.test.com",
            classification="test_classification",
            datestamp=datetime.datetime.now()
        )

        responce = self.client.get(reverse('showresults'))

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/results.html')

    def test_showresults_DELETE(self):
        
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

        PredictedWebsites.objects.create(
            url="https://www.test.com",
            classification="test_classification",
            datestamp=datetime.datetime.now()
        )

        responce = self.client.post(reverse('showresults'), {
            'id': 1
        })

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/noResults.html')
        self.assertEqual(PredictedWebsites.objects.count(), 0)
        